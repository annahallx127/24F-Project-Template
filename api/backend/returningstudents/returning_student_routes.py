from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object for returning students
returning_student = Blueprint('returning_student', __name__)

@returning_student.route('/availabilities', methods=['GET'])
def get_availabilities():
    """
    Fetch all availabilities for a hardcoded StudentID.
    """
    cursor = db.get_db().cursor()

    query = '''
        SELECT AvailabilityID, StudentID, StartDate, EndDate 
        FROM Availabilities 
        WHERE StudentID = %s;
    '''

        # Execute query for the hardcoded StudentID
    cursor.execute(query, (2,)) 
    availabilities = cursor.fetchall()

        # If no availabilities found, return a 404 response
    if not availabilities:
        return jsonify({"error": "No availabilities found"}), 404

  
      # Return the student data as a JSON response
    the_response = make_response(jsonify(availabilities))
    the_response.status_code = 200
    return the_response

@returning_student.route('/availabilities/<int:availability_id>', methods=['PUT'])
def update_availability(availability_id):
    current_app.logger.info(f"PUT /availabilities/{availability_id} route")
    
    try:
        # Parse request body
        availability_info = request.json
        current_app.logger.info(f"Received payload: {availability_info}")

        if not availability_info:
            raise ValueError("Request body is empty or invalid JSON")

        # Check if the availability exists
        cursor = db.get_db().cursor()
        cursor.execute('SELECT StudentID FROM Availabilities WHERE AvailabilityID = %s', (availability_id,))
        result = cursor.fetchone()

        if not result or result['StudentID'] != 2:
            return jsonify({'message': 'Availability not found or unauthorized'}), 404

        # Prepare the update query
        updates = []
        values = []
        if 'StartDate' in availability_info:
            updates.append("StartDate = %s")
            values.append(availability_info['StartDate'])
        if 'EndDate' in availability_info:
            updates.append("EndDate = %s")
            values.append(availability_info['EndDate'])

        if updates:
            query = f"UPDATE Availabilities SET {', '.join(updates)} WHERE AvailabilityID = %s"
            values.append(availability_id)
            cursor.execute(query, tuple(values))
            db.get_db().commit()
            return jsonify({'message': 'Availability updated successfully'}), 200
        else:
            return jsonify({'message': 'No fields to update provided'}), 400
    except ValueError as ve:
        current_app.logger.error(f"ValueError: {ve}")
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating availability: {str(e)}")
        return jsonify({'message': 'Failed to update availability', 'details': str(e)}), 500

# post availability for other students/mentees to view
@returning_student.route('/availabilities', methods=['POST'])
def post_availability():
    current_app.logger.info("POST /availabilities route")

    try:
        # Parse the request body
        availability_info = request.json
        current_app.logger.info(f"Received payload: {availability_info}")

        # Validate required fields
        required_fields = ['StudentID', 'StartDate', 'EndDate']
        for field in required_fields:
            if field not in availability_info:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        student_id = availability_info['StudentID']
        StartDate = availability_info['StartDate']
        EndDate = availability_info['EndDate']

        # Validate that StudentID is 2 (or modify logic if necessary)
        if student_id != 2:
            return jsonify({'message': 'Unauthorized: Can only post availability for StudentID 2'}), 403

        # Insert into the database
        cursor = db.get_db().cursor()
        query = '''
            INSERT INTO Availabilities (StudentID, StartDate, EndDate)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (student_id, StartDate, EndDate))
        db.get_db().commit()

        # Return a success message
        return jsonify({'message': 'Availability posted successfully'}), 201

    except Exception as e:
        current_app.logger.error(f"Error posting availability: {str(e)}")
        return jsonify({'message': 'Failed to post availability', 'details': str(e)}), 500

# delete availability for coffee chat
@returning_student.route('/availabilities/<int:availability_id>', methods=['DELETE'])
def delete_availability(availability_id):
    current_app.logger.info(f"DELETE /availabilities/{availability_id} route")

    try:
        # Check if the availability exists
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Availabilities WHERE AvailabilityID = %s', (availability_id,))
        result = cursor.fetchone()

        if not result:
            current_app.logger.error(f"Availability with ID {availability_id} not found.")
            return jsonify({'message': f'Availability with ID {availability_id} not found'}), 404

        # Delete the availability
        query = 'DELETE FROM Availabilities WHERE AvailabilityID = %s'
        cursor.execute(query, (availability_id,))
        db.get_db().commit()

        current_app.logger.info(f"Availability with ID {availability_id} deleted successfully.")
        return jsonify({'message': f'Availability with ID {availability_id} deleted successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting availability: {str(e)}")
        return jsonify({'message': 'Failed to delete availability', 'details': str(e)}), 500


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