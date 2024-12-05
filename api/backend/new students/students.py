########################################################
# New students blueprint of endpoints
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
new_students = Blueprint('new students', __name__)


#------------------------------------------------------------
# Get all new students from the system
@new_students.route('/students/new_student', methods=['GET'])
def get_new_student():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, FirstName, LastName, Major, WCFI
                   FROM Student
                   WHERE isMentor = False
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update student info for student with particular StudentID
#   Notice the manner of constructing the query.
#------------------------------------------------------------
# Update student info for student using StudentID from request body
@new_students.route('/students/new_student', methods=['PUT'])
def update_new_student():
    current_app.logger.info('PUT /students/new_student route')
    
    # Parse the request body
    student_info = request.json
    
    # Extract fields from the request body
    student_id = student_info['StudentID']  # Ensure StudentID is included
    if not student_id:
        return jsonify({'message': 'StudentID is required'}), 400

    # Extract fields to update
    first_name = student_info['FirstName']
    last_name = student_info[('LastName')]
    major = student_info[('Major')]
    is_mentor = student_info[('isMentor')]
    wcfi = student_info[('WCFI')]

    # Step 1: Check if the student is a "new student" (isMentor = false)
    cursor = db.get_db().cursor()
    cursor.execute("SELECT isMentor FROM Student WHERE StudentID = %s", (student_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'message': 'Student not found'}), 404

    if result[0]:  # `isMentor` is true
        return jsonify({'message': 'Cannot update this student as they are not a new student'}), 403

    # Step 2: Prepare the update query dynamically
    updates = []
    values = []

    if first_name:
        updates.append("FirstName = %s")
        values.append(first_name)
    if last_name:
        updates.append("LastName = %s")
        values.append(last_name)
    if major:
        updates.append("Major = %s")
        values.append(major)
    if is_mentor is not None:  # Allow updates to isMentor if explicitly set
        updates.append("isMentor = %s")
        values.append(is_mentor)
    if wcfi:
        updates.append("WCFI = %s")
        values.append(wcfi)

    # Combine the updates into a single SQL query
    if updates:
        query = 'UPDATE Student SET {', '.join(updates)} WHERE StudentID = %s'
        values.append(student_id)  # Add StudentID as the last parameter for the WHERE clause

        cursor.execute(query, tuple(values))
        db.get_db().commit()

        return jsonify({'message': 'Student updated successfully'}), 200
    else:
        return jsonify({'message': 'No fields to update provided'}), 400



# #------------------------------------------------------------
# Get student detail for student with particular StudentID
#   Notice the manner of constructing the query. 
@new_students.route('/students/new_student/<StudentID>', methods=['GET'])
def get_student(StudentID):
    current_app.logger.info('GET /students/new_student/<StudentID> route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT StudentID, FirstName, LastName, Major, isMentor, WCFI
        FROM Student
        WHERE StudentID = %s
    ''')

    student = cursor.fetchone()
    
    
    # If the student does not exist, return an error message
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    # Format the data as a dictionary to send as JSON
    student_data = {
        'StudentID': student[0],
        'FirstName': student[1],
        'LastName': student[2],
        'Major': student[3],
        'isMentor': student[4],
        'WCFI': student[5]
    }

    return jsonify(student_data), 200

#------------------------------------------------------------
# Get detailed information about a specific job posting by ID
@new_students.route('/job-listings/JobListingID>', methods=['GET'])
def get_job_listing_details(JobListingID):
    current_app.logger.info('GET /job-listings/{JobListingID} route')

    # Create a cursor to execute the query
    cursor = db.get_db().cursor()

    # SQL query to fetch job details based on the job ID
    query = '''
        SELECT 
            JobListingID, 
            CompanyID, 
            Job Description, 
            JobPositionTitle, 
            JobIsActive
        FROM JobListing
        WHERE JobID = %s
    '''
    cursor.execute(query, (id,))

    # Fetch the result
    job_listing = cursor.fetchone()

    # If no job posting is found, return an error message
    if not job_listing:
        return jsonify({'message': 'Job listing not found'}), 404

    # Format the result into a dictionary for JSON response
    job_data = {
        'JobID': job_listing[0],
        'CompanyID': job_listing[1],
        'Job Description': job_listing[3],
        'JobPositionTitle': job_listing[4],
        'JobIsActive': job_listing[5],
    }

    return jsonify(job_data), 200

#------------------------------------------------------------
# Withdraw a job application for a specific student
@new_students.route('/applications/{id}/withdraw', methods=['DELETE'])
def withdraw_application(id):
    current_app.logger.info('DELETE /applications/{id}/withdraw route')

    # Step 1: Check if the application exists
    cursor = db.get_db().cursor()
    query = "SELECT ApplicationID, StudentID, AppliedDate, Status, JobID FROM Application WHERE ApplicationID = %s"
    cursor.execute(query, (id,))
    application = cursor.fetchone()

    if not application:
        return jsonify({'message': 'Application not found'}), 404

    # Step 2: Check if the application is already withdrawn
    if application[1] == 'withdrawn':
        return jsonify({'message': 'Application has already been withdrawn'}), 400

    # Step 3: Update the application status to 'withdrawn'
    update_query = "UPDATE Applicatios SET Status = 'withdrawn' WHERE ApplicationID = %s"
    cursor.execute(update_query, (id,))
    db.get_db().commit()

    # Step 4: Return a success response
    return jsonify({'message': 'Application withdrawn successfully'}), 200

#------------------------------------------------------------
# Schedule a coffee chat by creating an appointment between a mentor and mentee
@new_students.route('/coffee-chat', methods=['POST'])
def schedule_coffee_chat():
    current_app.logger.info('POST /coffee-chat route')

    # Get the data from the request body
    chat_info = request.json
    mentor_id = chat_info['MentorID']
    mentee_id = chat_info['MenteeID']
    availability_id = chat_info['AvailabilityID']  # Availability ID for the mentor's time slot
    appointment_date = chat_info['AppointmentDate']  # Date and time for the coffee chat
    duration = chat_info['Duration']  # Duration of the chat in minutes
    meeting_subject = chat_info['MeetingSubject']  # Subject of the meeting

    # Step 1: Check if the availability slot exists
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM Availabilities WHERE AvailabilityID = %s", (availability_id,))
    availability = cursor.fetchone()

    if not availability:
        return jsonify({'message': 'Availability slot not found'}), 404

    # Step 2: Check if the mentor and mentee are available at this time
    if availability['MenteeID'] != availability['MentorID']:
        return jsonify({'message': 'The mentor ID does not match the availability'}), 400

    # Step 3: Create a new appointment (coffee chat) between the mentor and mentee
    cursor.execute("""
        INSERT INTO Appointment (MentorID, MenteeID, AvailabilityID, AppointmentDate, Duration, MeetingSubject)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (mentor_id, mentee_id, availability_id, appointment_date, duration, meeting_subject))
    db.get_db().commit()

    # Step 4: Return success message
    return jsonify({'message': 'Coffee chat scheduled successfully'}), 201

#------------------------------------------------------------
# Change application details (e.g., rank candidates, update resume)
@new_students.route('/applications/<application_id>', methods=['PUT'])
def update_application(application_id):
    current_app.logger.info(f'PUT /applications/{application_id} route')

    # Get the data from the request body
    application_info = request.json
    rank = application_info.get('rank')
    status = application_info.get('status')
    resume_id = application_info.get('resume_id')  # Optional, for updating the resume

    cursor = db.get_db().cursor()

    # Step 1: Check if the application exists
    cursor.execute("SELECT * FROM Application WHERE ApplicationID = %s", (application_id,))
    application = cursor.fetchone()

    if not application:
        return jsonify({'message': 'Application not found'}), 404

    # Step 2: Prepare the update query for application details
    updates = []
    values = []

    if rank is not None:
        updates.append("Rank = %s")
        values.append(rank)
    if status:
        updates.append("Status = %s")
        values.append(status)

    # Step 3: Prepare the update query for resume details if provided
    if resume_id:
        cursor.execute("SELECT * FROM Resume WHERE ResumeID = %s", (resume_id,))
        resume = cursor.fetchone()

        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        # Check if the resume belongs to the same student
        cursor.execute("SELECT StudentID FROM Application WHERE ApplicationID = %s", (application_id,))
        student_id = cursor.fetchone()[0]

        if student_id != resume['StudentID']:
            return jsonify({'message': 'Resume does not belong to the student of this application'}), 403

        updates.append("ResumeID = %s")
        values.append(resume_id)

    # Step 4: Execute the application update query
    if updates:
        query = f"UPDATE Application SET {', '.join(updates)} WHERE ApplicationID = %s"
        values.append(application_id)  # Add ApplicationID as the last parameter for the WHERE clause

        cursor.execute(query, tuple(values))
        db.get_db().commit()

        # Return success message
        return jsonify({'message': 'Application updated successfully'}), 200
    else:
        return jsonify({'message': 'No fields to update provided'}), 400
