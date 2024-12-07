########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
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
hiring_manager = Blueprint('hiring_manager', __name__)
#------------------------------------------------------------
# Get all candidates who applied for a specific job
@hiring_manager.route('/job-listings/<int:job_id>/candidates', methods=['GET'])
def get_candidates_by_job(job_id):
    cursor = db.get_db().cursor()
    
    # SQL query to fetch candidates for the job listing
    query = '''
        SELECT c.CandidateID, c.FirstName, c.LastName, c.Email, c.ApplicationStage
        FROM Candidate c
        WHERE c.AppliedJobID = %s
    '''
    try:
        cursor.execute(query, (job_id,))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Convert rows into a list of dictionaries
        result = [dict(zip(column_names, row)) for row in rows]
        
        if result:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"message": f"No candidates found for job ID {job_id}"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


  #GET WCFI  
@hiring_manager.route('/job-listings/<int:job_id>/candidates-wcfi', methods=['GET'])
def get_candidates_wcfi(job_id):
    """
    Fetch WCFI values, First Name, Last Name, and Status for students who applied for a specific job.
    """
    cursor = db.get_db().cursor()

    # Query to fetch FirstName, LastName, WCFI, and Status for candidates applied to the specified job ID
    query = '''
        SELECT DISTINCT s.FirstName, s.LastName, s.WCFI, a.Status
        FROM Student s
        JOIN Application a ON s.StudentID = a.StudentID
        WHERE a.JobID = %s
    '''

    try:
        # Execute the query with the provided job_id
        cursor.execute(query, (job_id,))
        rows = cursor.fetchall()

        if rows:
            # Include WCFI and Status in the response
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"message": f"No candidates found for Job ID {job_id}"}), 404)

    except Exception as e:
        current_app.logger.error(f"Error fetching candidates' WCFI: {e}")
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)



# Update a job listing based on JobListingID 
@hiring_manager.route('/hiring-manager/job-listings/<int:job_id>', methods=['PUT'])
def update_job_listing(job_id):
    """
    Update an existing job listing by JobListingID, hardcoding the CompanyID for Miles Morales.
    """
    try:
        # Parse the request payload
        job_data = request.get_json()

        # Validate JobIsActive if provided
        if 'JobIsActive' in job_data:
            job_is_active = job_data['JobIsActive']
            if not isinstance(job_is_active, bool):
                return jsonify({'message': 'JobIsActive must be a boolean'}), 400

        # Hardcoded CompanyID for SpiderVerse
        company_id = 1  # Based on insert statements

        # Build the update query
        updates = []
        values = []

        if 'JobPositionTitle' in job_data:
            updates.append("JobPositionTitle = %s")
            values.append(job_data['JobPositionTitle'])
        if 'JobDescription' in job_data:
            updates.append("JobDescription = %s")
            values.append(job_data['JobDescription'])
        if 'JobIsActive' in job_data:
            updates.append("JobIsActive = %s")
            values.append(job_data['JobIsActive'])

        # Ensure there are fields to update
        if not updates:
            return jsonify({'message': 'No fields to update provided'}), 400

        # Finalize the update query with a check for CompanyID
        query = f"""
            UPDATE JobListings 
            SET {', '.join(updates)}
            WHERE JobListingID = %s AND CompanyID = %s
        """
        values.extend([job_id, company_id])

        # Execute the update
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(values))
        db.get_db().commit()

        # Check if the update affected any rows
        if cursor.rowcount == 0:
            return jsonify({'message': f'Job listing with ID {job_id} not found or not associated with the company'}), 404

        return jsonify({'message': 'Job listing updated successfully!'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating job listing: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Delete a job listing based on JobListingID
@hiring_manager.route('/hiring-manager/job-listings/<int:job_id>', methods=['DELETE'])
def delete_job_listing(job_id):
    """
    Delete a job listing by JobListingID, ensuring it belongs to Miles Morales' company (CompanyID = 1).
    """
    try:
        # Hardcoded CompanyID for SpiderVerse
        company_id = 1  # Based on insert statements

        # SQL query to delete the job listing, ensuring it belongs to the correct company
        query = '''
            DELETE FROM JobListings
            WHERE JobListingID = %s AND CompanyID = %s
        '''

        cursor = db.get_db().cursor()
        cursor.execute(query, (job_id, company_id))
        db.get_db().commit()

        # Check if a row was deleted
        if cursor.rowcount == 0:
            return jsonify({
                "message": f"Job listing with ID {job_id} not found or not associated with the company."
            }), 404

        return jsonify({
            "message": f"Job listing with ID {job_id} successfully deleted."
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting job listing: {e}")
        db.get_db().rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Get the ranking of candidates for a specific job listing
@hiring_manager.route('/job-listings/<int:job_id>/candidates-ranking', methods=['GET'])
def get_candidates_ranking_for_job(job_id):
    cursor = db.get_db().cursor()

    # SQL query to get candidate ranking for a specific job listing
    query = '''
        SELECT s.StudentID, s.FirstName, s.LastName, r.RankNum, j.JobPositionTitle
        FROM Rank r
        JOIN Student s ON r.ApplicantID = s.StudentID
        JOIN Application a ON a.StudentID = s.StudentID
        JOIN JobListings j ON a.JobID = j.JobListingID
        WHERE j.JobListingID = %s
        ORDER BY r.RankNum ASC
    '''
    try:
        cursor.execute(query, (job_id,))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows into a list of dictionaries
        result = [dict(zip(column_names, row)) for row in rows]

        if result:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"message": f"No rankings found for job ID {job_id}"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
# Get the list of all candidates with their rankings
@hiring_manager.route('/candidates-ranking', methods=['GET'])
def get_all_candidates_ranking():
    cursor = db.get_db().cursor()

    # SQL query to get all candidate rankings
    query = '''
        SELECT s.StudentID, s.FirstName, s.LastName, r.RankNum
        FROM Rank r
        JOIN Student s ON r.ApplicantID = s.StudentID
        ORDER BY r.RankNum ASC
    '''
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows into a list of dictionaries
        result = [dict(zip(column_names, row)) for row in rows]

        if result:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"message": "No candidates found"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@hiring_manager.route('/job-listings', methods=['GET'])
def get_job_listings():
    current_app.logger.info(f'GET /job-listings route')
    
    cursor = db.get_db().cursor()
    query = "SELECT * FROM JobListings"
    cursor.execute(query)
    job_listings = cursor.fetchall()

    if not job_listings:
        return jsonify({'message': 'No job listings available'}), 404
    
    # Return the student data as a JSON response
    the_response = make_response(jsonify(job_listings))
    the_response.status_code = 200
    return the_response

