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

"-------------------------------------------------------------------------------------------------------------------"
@returning_student.route('/completed_coops', methods=['GET'])
def fetch_completed_coops():
    current_app.logger.info(f"GET /completed_coops route")

    try:
        cursor = db.get_db().cursor()  # Ensure rows are returned as dictionaries
        cursor.execute('''
        SELECT *
        FROM Coop
        WHERE StudentID= %s
        ''', (2,))
    
    # Fetch the student data
        coops = cursor.fetchall()
    
        return jsonify(coops), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching completed co-ops: {str(e)}")
        return jsonify({'message': 'Failed to fetch completed co-ops', 'details': str(e)}), 500

@returning_student.route('/coop-review', methods=['POST'])
def post_coop_review():
    """
    Add a co-op review by CoopID and StudentID
    """
    current_app.logger.info(f"POST /coop-review route")

    try:
        # Parse the request JSON
        data = request.json

        # Validate input fields
        required_fields = ['CoopID', 'StudentID', 'CoopReview', 'CoopRating']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # Extract fields from the request
        coop_id = data['CoopID']
        student_id = data['StudentID']
        coop_review = data['CoopReview']
        coop_rating = data['CoopRating']

        # Ensure the review is being added only for StudentID = 2
        if student_id != 2:
            return jsonify({'message': 'Unauthorized: Can only post review for StudentID = 2'}), 403

        # Update the review in the database
        cursor = db.get_db().cursor()
        query = '''
            UPDATE Coop 
            SET CoopReview = %s, CoopRating = %s 
            WHERE CoopID = %s AND StudentID = %s
        '''
        cursor.execute(query, (coop_review, coop_rating, coop_id, student_id))
        db.get_db().commit()

        current_app.logger.info(f"Co-op review for CoopID {coop_id} added/updated successfully.")
        return jsonify({'message': 'Co-op review posted successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error posting co-op review: {str(e)}")
        return jsonify({'message': 'Failed to post co-op review', 'details': str(e)}), 500


@returning_student.route('/coop-review', methods=['DELETE'])
def delete_coop_review():
    """
    Delete a co-op review by CoopID for StudentID = 2
    """
    current_app.logger.info("DELETE /coop-review route")

    try:
        # Parse the request JSON
        data = request.get_json()
        coop_id = data.get('CoopID')

        # Validate input
        if not coop_id:
            return jsonify({'message': 'Missing required field: CoopID'}), 400

        # Hardcoded to allow only StudentID = 2
        student_id = 2

        # Connect to the database
        cursor = db.get_db().cursor()

        # Check if the review exists for StudentID = 2 and the given CoopID
        cursor.execute("""
            SELECT CoopID 
            FROM Coop 
            WHERE CoopID = %s AND StudentID = %s
        """, (coop_id, student_id))
        review = cursor.fetchone()

        if not review:
            current_app.logger.error(f"No review found for CoopID: {coop_id} and StudentID: {student_id}")
            return jsonify({'message': 'Review not found or unauthorized'}), 404

        # Delete the review by nullifying CoopReview and CoopRating
        cursor.execute("""
            UPDATE Coop 
            SET CoopReview = NULL, CoopRating = NULL 
            WHERE CoopID = %s AND StudentID = %s
        """, (coop_id, student_id))
        db.get_db().commit()

        current_app.logger.info(f"Review for CoopID {coop_id} and StudentID {student_id} deleted successfully")
        return jsonify({'message': 'Co-op review deleted successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting co-op review: {str(e)}")
        return jsonify({'message': 'Failed to delete co-op review', 'details': str(e)}), 500
