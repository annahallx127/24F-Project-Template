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
new_students = Blueprint('new_students', __name__)


# #------------------------------------------------------------
# Get student detail for student with particular StudentID
#   Notice the manner of constructing the query. 
@new_students.route('/students/new_student', methods=['GET'])
def get_student():
    current_app.logger.info(f"GET /students/new_student route")

    # Get the database cursor
    cursor = db.get_db().cursor()
    
    # Execute the query to fetch student details
    cursor.execute('''
    SELECT *
    FROM Student
    WHERE FirstName = %s
    ''', ('Peter',))
    
    # Fetch the student data
    student = cursor.fetchone()
    
    # If the student does not exist, return an error message
    if not student:
        current_app.logger.error(f"Student Information not found.")
        return jsonify({'message': 'Student not found'}), 404

    # Return the student data as a JSON response
    the_response = make_response(jsonify(student))
    the_response.status_code = 200
    return the_response

# #------------------------------------------------------------
# Update student detail for student with particular StudentID
@new_students.route('/students/new_student/<StudentID>', methods=['PUT'])
def update_new_student(StudentID):
    current_app.logger.info('PUT /students/new_student/<StudentID> route')
    
    # Parse the request body
    student_info = request.json
    
    # # Check if the student exists and if they are not a mentor
    cursor = db.get_db().cursor()
 
    # Prepare the update query
    updates = []
    values = []

    if 'FirstName' in student_info:
        updates.append("FirstName = %s")
        values.append(student_info['FirstName'])
    if 'LastName' in student_info:
        updates.append("LastName = %s")
        values.append(student_info['LastName'])
    if 'Major' in student_info:
        updates.append("Major = %s")
        values.append(student_info['Major'])
    if 'WCFI' in student_info:
        updates.append("WCFI = %s")
        values.append(student_info['WCFI'])

    if updates:
        query = f"UPDATE Student SET {', '.join(updates)} WHERE StudentID = %s"
        values.append(StudentID)
        cursor.execute(query, tuple(values))
        db.get_db().commit()

        return jsonify({'message': 'Student updated successfully'}), 200
    else:
        return jsonify({'message': 'No fields to update provided'}), 400


#------------------------------------------------------------
# Get all job listings
@new_students.route('/job-listings', methods=['GET'])
def get_all_job_listings():
    current_app.logger.info('GET /job-listings route')
    
    # Create a cursor to execute the query
    cursor = db.get_db().cursor()
    
    # Query to retrieve all job listings
    query = '''
        SELECT *
        FROM JobListing
    '''
    cursor.execute(query)
    
    # Fetch all job listings
    job_listings = cursor.fetchall()
    
    # If no job listings are found, return an appropriate response
    if not job_listings:
        return jsonify({'message': 'No job listings found'}), 404
    
    # Format the job listings as a list of dictionaries
    job_data = []
    for job in job_listings:
        job_data.append({
            'JobListingID': job[0],
            'CompanyID': job[1],
            'JobDescription': job[2],
            'JobPositionTitle': job[3],
            'JobIsActive': job[4],
        })
    
    # Return the list of job listings as a JSON response
    return jsonify({'job_listings': job_data}), 200


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
    cursor.execute(query, (JobListingID,))

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
# Apply for a job
@new_students.route('/applications', methods=['POST'])
def apply_for_job():
    current_app.logger.info('POST /applications route')
    
    # Get the request data
    application_data = request.json
    student_id = application_data.get('StudentID')
    job_id = application_data.get('JobID')
    status = application_data.get('Status')

    # Validate the incoming data
    if not student_id or not job_id or not status:
        return jsonify({'message': 'Missing required fields'}), 400

    # Get the current date for the AppliedDate
    applied_date = datetime.utcnow()

    # Insert the application into the database
    cursor = db.get_db().cursor()
    cursor.execute("""
        INSERT INTO Application (StudentID, AppliedDate, Status, JobID)
        VALUES (%s, %s, %s, %s)
    """, (student_id, applied_date, status, job_id))
    
    db.get_db().commit()

    return jsonify({'message': 'Application submitted successfully'}), 201


#------------------------------------------------------------
# Get all the jobs a student has applied for
@new_students.route('/applications/', methods=['GET'])
def get_student_applications():
    current_app.logger.info(f'GET /applications/ route')
    
    # Query to get all job details for a student
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT j.JobListingID, j.JobPositionTitle, j.JobDescription, a.Status, a.AppliedDate
        FROM Application a
        JOIN JobListings j ON a.JobID = j.JobListingID
        WHERE a.FirstName = %s
    """, ('Peter',))
    
    # Fetch all results
    applications = cursor.fetchall()

    # If no applications found for the student
    if not applications:
        return jsonify({'message': 'No applications found for this student'}), 404
    

    # Return the lisst of jobs as a JSON response
    the_response = make_response(jsonify(applications))
    the_response.status_code = 200
    return the_response


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
    update_query = "UPDATE Application SET Status = 'withdrawn' WHERE ApplicationID = %s"
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

# Define the upload folder for resume storage (change this path as necessary)
UPLOAD_FOLDER = '/path/to/your/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'rtf'}

# Helper function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#------------------------------------------------------------
# Submit a resume for a student
@new_students.route('/resume/<int:student_id>', methods=['POST'])
def submit_resume(student_id):
    current_app.logger.info(f'POST /resume/{student_id} route')
    
    # Ensure a file is part of the request
    if 'resume' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['resume']
    
    # Check if a file is selected and has a valid extension
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save the resume file
        filename = f"{student_id}_resume.{file.filename.rsplit('.', 1)[1].lower()}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Insert resume details into the database
        resume_info = request.json
        work_experience = resume_info.get('WorkExperience')
        technical_skills = resume_info.get('TechnicalSkills')
        soft_skills = resume_info.get('SoftSkills')
        resume_name = resume_info.get('ResumeName', filename)

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Resume (StudentID, WorkExperience, ResumeName, TechnicalSkills, SoftSkills)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, work_experience, resume_name, technical_skills, soft_skills))
        
        db.get_db().commit()

        return jsonify({'message': 'Resume submitted successfully'}), 200
    else:
        return jsonify({'message': 'Invalid file format'}), 400
    
    #------------------------------------------------------------
# Delete a student's resume
@new_students.route('/resume/<int:student_id>', methods=['DELETE'])
def delete_resume(student_id):
    current_app.logger.info(f'DELETE /resume/{student_id} route')
    
    # Retrieve the resume record from the database
    cursor = db.get_db().cursor()
    cursor.execute("SELECT ResumeID, ResumeName FROM Resume WHERE StudentID = %s", (student_id,))
    resume = cursor.fetchone()

    # If no resume found for the student
    if not resume:
        return jsonify({'message': 'No resume found for this student'}), 404

    # Delete the resume file from the server
    file_path = os.path.join(UPLOAD_FOLDER, resume[1])
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the resume record from the database
    cursor.execute("DELETE FROM Resume WHERE StudentID = %s", (student_id,))
    db.get_db().commit()

    return jsonify({'message': 'Resume deleted successfully'}), 200
