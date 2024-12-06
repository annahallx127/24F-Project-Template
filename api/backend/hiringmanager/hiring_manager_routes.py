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

# Get MBTI distribution for all candidates of a specific job
@hiring_manager.route('/job-listings/<int:job_id>/mbti-distribution', methods=['GET'])
def get_mbti_distribution(job_id):
    cursor = db.get_db().cursor()
    
    # SQL query to fetch MBTI results for candidates of a specific job
    query = '''
        SELECT MBTIResult, COUNT(*) as Count
        FROM Candidate
        WHERE AppliedJobID = %s
        GROUP BY MBTIResult
    '''
    try:
        cursor.execute(query, (job_id,))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Convert rows into a list of dictionaries
        result = [dict(zip(column_names, row)) for row in rows]
        
        return make_response(jsonify(result), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
#Post job listing    
@hiring_manager.route('/hiring-manager/job-listings', methods=['POST'])
def post_job_listing():
    current_app.logger.info('POST /hiring-manager/job-listings route')

    job_data = request.json
    required_fields = ['HiringManagerID', 'JobPositionTitle', 'JobDescription', 'JobIsActive']

    # Validate input fields
    if not all(field in job_data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    # Ensure JobIsActive is a valid boolean
    job_is_active = job_data['JobIsActive']
    if not isinstance(job_is_active, (bool, int)) or job_is_active not in [True, False, 1, 0]:
        return jsonify({'message': 'JobIsActive must be a boolean'}), 400

    cursor = db.get_db().cursor()
    cursor.execute("""
        INSERT INTO JobListing (HiringManagerID, JobPositionTitle, JobDescription, JobIsActive)
        VALUES (%s, %s, %s, %s)
    """, (job_data['HiringManagerID'], job_data['JobPositionTitle'], job_data['JobDescription'], bool(job_is_active)))
    db.get_db().commit()

    return jsonify({'message': 'Job listing created successfully'}), 201

# Update a job listing based on JobListingID 
@hiring_manager.route('/hiring-manager/job-listings/<int:job_id>', methods=['PUT'])
def update_job_listing(job_id):
    current_app.logger.info(f'PUT /hiring-manager/job-listings/{job_id} route')

    job_data = request.json
    updates = []
    values = []

    if 'JobPositionTitle' in job_data:
        updates.append("JobPositionTitle = %s")
        values.append(job_data['JobPositionTitle'])
    if 'JobDescription' in job_data:
        updates.append("JobDescription = %s")
        values.append(job_data['JobDescription'])
    if 'JobIsActive' in job_data:
        # Ensure JobIsActive is a valid boolean
        job_is_active = job_data['JobIsActive']
        if not isinstance(job_is_active, (bool, int)) or job_is_active not in [True, False, 1, 0]:
            return jsonify({'message': 'JobIsActive must be a boolean'}), 400
        updates.append("JobIsActive = %s")
        values.append(bool(job_is_active))

    if updates:
        query = f"UPDATE JobListing SET {', '.join(updates)} WHERE JobListingID = %s"
        values.append(job_id)
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(values))
        db.get_db().commit()
        return jsonify({'message': 'Job listing updated successfully'}), 200
    else:
        return jsonify({'message': 'No fields to update provided'}), 400


# Delete a job listing based on JobListingID
@hiring_manager.route('/job-listings/<int:id>', methods=['DELETE'])
def delete_job_listing(id):
    cursor = db.get_db().cursor()

    # SQL query to delete the job listing
    query = '''
        DELETE FROM JobListing
        WHERE JobListingID = %s
    '''

    try:
        cursor.execute(query, (id,))
        db.get_db().commit()

        # Check if a row was deleted
        if cursor.rowcount == 0:
            return make_response(
                jsonify({"error": f"No job listing found with JobListingID {id}"}), 404
            )

        return make_response(
            jsonify({"message": f"Job listing with JobListingID {id} successfully deleted"}), 200
        )
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({"error": "Failed to delete job listing", "details": str(e)}), 500
        )

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
