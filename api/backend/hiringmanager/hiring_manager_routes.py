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
# Get all hiring managers from the system
@hiring_manager.route('/hiring-managers', methods=['GET'])
def get_all_hiring_managers():
    cursor = db.get_db().cursor()
    
    # SQL query to fetch all hiring managers
    query = '''
        SELECT * FROM HiringManager
    '''
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Convert rows into a list of dictionaries
        result = [dict(zip(column_names, row)) for row in rows]
        
        return make_response(jsonify(result), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
# add a new hiring manager to the system 
@hiring_manager.route('/hiring-managers', methods=['POST'])
def add_hiring_manager():
    cursor = db.get_db().cursor()
    req_data = request.get_json()
    first_name = req_data.get('FirstName')
    last_name = req_data.get('LastName')
    email = req_data.get('Email')
    company_id = req_data.get('CompanyID')

    if not all([first_name, last_name, email, company_id]):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = '''
        INSERT INTO HiringManager (FirstName, LastName, Email, CompanyID)
        VALUES (%s, %s, %s, %s)
    '''
    try:
        cursor.execute(query, (first_name, last_name, email, company_id))
        db.get_db().commit()
        return make_response(jsonify({"message": "Hiring manager added successfully"}), 201)
    except Exception as e:
        db.get_db().rollback()
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

#Update applicant MBTI 
@hiring_manager.route('/applicants/<int:applicant_id>/mbti', methods=['PUT'])
def update_applicant_mbti(applicant_id):
    data = request.get_json()
    mbti_type = data.get('MBTIType')
    if not mbti_type:
        return make_response(jsonify({"error": "Missing MBTIType field"}), 400)

    query = '''
        UPDATE Applicant 
        SET MBTIType = %s
        WHERE ApplicantID = %s
    '''
    cursor = db.get_db().cursor()
    try:
        cursor.execute(query, (mbti_type, applicant_id))
        db.get_db().commit()
        if cursor.rowcount == 0:
            return make_response(jsonify({"error": "Applicant not found"}), 404)
        return make_response(jsonify({"message": "MBTI updated successfully"}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({"error": str(e)}), 500)
