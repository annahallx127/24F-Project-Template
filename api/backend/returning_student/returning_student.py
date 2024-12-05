
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

# Post a co-op review after completing co-op
@returning_student.route('/coop/review/<int:coopId>', methods=['PUT'])
def update_coop_review(coopId):
    cursor = db.get_db().cursor()
    req_data = request.get_json()

    review = req_data.get('CoopReview')
    rating = req_data.get('CoopRating')

    if not review or not isinstance(review, str) or len(review.strip()) == 0:
        return make_response(
            jsonify({"error": "CoopReview must be a non-empty string"}), 400
        )
    if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
        return make_response(
            jsonify({"error": "CoopRating must be an integer between 1 and 5"}), 400
        )

    query = '''
        UPDATE Coop
        SET CoopReview = %s, CoopRating = %s
        WHERE CoopID = %s
    '''
    try:
        cursor.execute(query, (review, rating, coopId))
        db.get_db().commit()
        return make_response(
            jsonify({"message": "Co-op review updated successfully!"}), 200
        )
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({"error": "Failed to update co-op review", "details": str(e)}), 500
        )

# update co-op review
@returning_student.route('/coop/review/<int:coopId>', methods=['PUT'])
def update_coop_review(coopId):
    cursor = db.get_db().cursor()
    req_data = request.get_json()

    review = req_data.get('CoopReview')
    rating = req_data.get('CoopRating')

    query = '''
        UPDATE Coop
        SET CoopReview = %s, CoopRating = %s
        WHERE CoopID = %s
    '''
    try:
        cursor.execute(query, (review, rating, coopId))
        db.get_db().commit()
        the_response = make_response(jsonify({"message": "Co-op review updated successfully!"}), 200)
    except Exception as e:
        db.get_db().rollback()
        the_response = make_response(jsonify({"error": str(e)}), 500)

    return the_response




