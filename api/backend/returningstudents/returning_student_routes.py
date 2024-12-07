from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import logging
from backend.ml_models.model01 import predict

# Create a new Blueprint object for returning students
returning_student = Blueprint('returning_student', __name__)

@returning_student.route('/availabilities', methods=['GET'])
def get_availabilities():
    """
    Fetch all availabilities for a hardcoded StudentID (e.g., Gwen Stacy).
    """
    cursor = db.get_db().cursor()

    query = '''
        SELECT AvailabilityID, StudentID, StartDate, EndDate 
        FROM Availabilities 
        WHERE StudentID = %s;
    '''

        # Execute query for the hardcoded StudentID
        cursor.execute(query, (2,))  # Replace `2` with Gwen Stacy's StudentID
        availabilities = cursor.fetchone()

        # If no availabilities found, return a 404 response
        if not availabilities:
            return jsonify({"error": "No availabilities found"}), 404

        # Convert rows into a JSON-serializable format, ensuring datetime fields are converted to strings
        results = [
            {
                "AvailabilityID": row[0],
                "StudentID": row[1],
                "StartDate": row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else None,
                "EndDate": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None
            }
            for row in availabilities
        ]

        return jsonify(results), 200

# # Post availability so other students can schedule coffee chat
# @returning_student.route('/availability', methods=['POST'])
# def post_availability():
#     cursor = db.get_db().cursor()

#     req_data = request.get_json()

#     student_id = req_data.get('StudentID')
#     start_date = req_data.get('StartDate')
#     end_date = req_data.get('EndDate')


#     if not student_id or not start_date or not end_date:
#         the_response = make_response(
#             jsonify({"error": "Missing required fields: StudentID, StartDate, EndDate"}), 400
#         )
#         return the_response


#     query = '''
#         INSERT INTO Availability (StudentID, StartDate, EndDate)
#         VALUES (%s, %s, %s)
#     '''

#     try:
#         cursor.execute(query, (student_id, start_date, end_date))
#         db.get_db().commit()
#         the_response = make_response(
#             jsonify({"message": "Availability successfully added!"}), 201
#         )
#     except Exception as e:
#         db.get_db().rollback()
#         the_response = make_response(
#             jsonify({"error": str(e)}), 500
#         )

#     return the_response

# # update availability for coffee chat
# @returning_student.route('/availability/<int:availabilityId>', methods=['PUT'])
# def update_availability(availabilityId):
#     cursor = db.get_db().cursor()
#     req_data = request.get_json()

#     start_date = req_data.get('StartDate')
#     end_date = req_data.get('EndDate')

#     query = '''
#         UPDATE Availability
#         SET StartDate = %s, EndDate = %s
#         WHERE AvailabilityID = %s
#     '''
#     try:
#         cursor.execute(query, (start_date, end_date, availabilityId))
#         db.get_db().commit()
#         the_response = make_response(jsonify({"message": "Availability updated successfully!"}), 200)
#     except Exception as e:
#         db.get_db().rollback()
#         the_response = make_response(jsonify({"error": str(e)}), 500)

#     return the_response

# # Post a co-op review after completing co-op
# @returning_student.route('/coop/review/<int:coopId>', methods=['POST'])
# def update_coop_review(coopId):
#     cursor = db.get_db().cursor()
#     req_data = request.get_json()

#     review = req_data.get('CoopReview')
#     rating = req_data.get('CoopRating')

#     if not review or not isinstance(review, str) or len(review.strip()) == 0:
#         return make_response(
#             jsonify({"error": "CoopReview must be a non-empty string"}), 400
#         )
#     if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
#         return make_response(
#             jsonify({"error": "CoopRating must be an integer between 1 and 5"}), 400
#         )

#     query = '''
#         UPDATE Coop
#         SET CoopReview = %s, CoopRating = %s
#         WHERE CoopID = %s
#     '''
#     try:
#         cursor.execute(query, (review, rating, coopId))
#         db.get_db().commit()
#         return make_response(
#             jsonify({"message": "Co-op review updated successfully!"}), 200
#         )
#     except Exception as e:
#         db.get_db().rollback()
#         return make_response(
#             jsonify({"error": "Failed to update co-op review", "details": str(e)}), 500
#         )

# # # update co-op review
# # @returning_student.route('/coop/review/<int:coopId>', methods=['PUT'])
# # def update_coop_review(coopId):
# #     cursor = db.get_db().cursor()
# #     req_data = request.get_json()

# #     review = req_data.get('CoopReview')
# #     rating = req_data.get('CoopRating')

# #     query = '''
# #         UPDATE Coop
# #         SET CoopReview = %s, CoopRating = %s
# #         WHERE CoopID = %s
# #     '''
# #     try:
# #         cursor.execute(query, (review, rating, coopId))
# #         db.get_db().commit()
# #         the_response = make_response(jsonify({"message": "Co-op review updated successfully!"}), 200)
# #     except Exception as e:
# #         db.get_db().rollback()
# #         the_response = make_response(jsonify({"error": str(e)}), 500)

# #     return the_response



# # delete a co-op review
# @returning_student.route('/coop/review/<int:coop_id>', methods=['DELETE'])
# def delete_coop_review(coop_id):
#     # Get the database cursor
#     cursor = db.get_db().cursor()

#     # SQL query to delete the co-op review based on CoopID
#     query = '''DELETE FROM Coop WHERE CoopID = %s'''

#     # Execute the query
#     try:
#         cursor.execute(query, (coop_id,))
#         db.get_db().commit()

#         # Check if a row was deleted
#         if cursor.rowcount == 0:
#             the_response = make_response(
#                 jsonify({"error": f" Co-op review with CoopID {coop_id} does not exist"}), 404
#             )
#         else:
#             the_response = make_response(
#                 jsonify({"message": f"Co-op review with CoopID {coop_id} successfully deleted!"}), 200
#             )
#     except Exception as e:
#         db.get_db().rollback()
#         the_response = make_response(
#             jsonify({"error": str(e)}), 500
#         )

#     return the_response


# # get all career projections
# @returning_student.route('/students/<int:studentId>/career-projections', methods=['GET'])
# def get_career_projections(studentId):
#     cursor = db.get_db().cursor()

#     # Query to fetch career projections for the student
#     query = '''
#         SELECT TimelineID, EducationTimeline, CoopTimeline, FullTimeTimeline
#         FROM CareerProjections
#         WHERE StudentID = %s
#     '''

#     try:
#         # Execute the query
#         cursor.execute(query, (studentId,))
#         theData = cursor.fetchone()

#         # If no career projections are found, return a 404
#         if not theData:
#             the_response = make_response(
#                 jsonify({"error": f"No career projections found for StudentID {studentId}"}), 404
#             )
#         else:
#             the_response = make_response(jsonify(theData), 200)

#     except Exception as e:
#         the_response = make_response(jsonify({"error": str(e)}), 500)

#     return the_response

