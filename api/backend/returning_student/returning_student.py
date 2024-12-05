
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
returning_student = Blueprint('returning_student', __name__)


#------------------------------------------------------------
# Get all returning students from the system
@returning_student.route('/students/returning', methods=['GET'])
def get_returning_students():
    cursor = db.get_db().cursor()

    # Modify the query to always filter for isMentor = true
    query = '''SELECT StudentID, FirstName, LastName, Major, isMentor 
               FROM Student
               WHERE isMentor = TRUE'''
    
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Post availability so other students can schedule coffee chat
@returning_student.route('/availability', methods=['POST'])
def post_availability():
    cursor = db.get_db().cursor()

    req_data = request.get_json()

    student_id = req_data.get('StudentID')
    start_date = req_data.get('StartDate')
    end_date = req_data.get('EndDate')


    if not student_id or not start_date or not end_date:
        the_response = make_response(
            jsonify({"error": "Missing required fields: StudentID, StartDate, EndDate"}), 400
        )
        return the_response


    query = '''
        INSERT INTO Availability (StudentID, StartDate, EndDate)
        VALUES (%s, %s, %s)
    '''

    try:
        cursor.execute(query, (student_id, start_date, end_date))
        db.get_db().commit()
        the_response = make_response(
            jsonify({"message": "Availability successfully added!"}), 201
        )
    except Exception as e:
        db.get_db().rollback()
        the_response = make_response(
            jsonify({"error": str(e)}), 500
        )

    return the_response

# update availability for coffee chat
@returning_student.route('/availability/<int:availabilityId>', methods=['PUT'])
def update_availability(availabilityId):
    cursor = db.get_db().cursor()
    req_data = request.get_json()

    start_date = req_data.get('StartDate')
    end_date = req_data.get('EndDate')

    query = '''
        UPDATE Availability
        SET StartDate = %s, EndDate = %s
        WHERE AvailabilityID = %s
    '''
    try:
        cursor.execute(query, (start_date, end_date, availabilityId))
        db.get_db().commit()
        the_response = make_response(jsonify({"message": "Availability updated successfully!"}), 200)
    except Exception as e:
        db.get_db().rollback()
        the_response = make_response(jsonify({"error": str(e)}), 500)

    return the_response





