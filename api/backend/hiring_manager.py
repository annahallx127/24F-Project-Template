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
@hiring_manager.route('/job-listings', methods=['POST'])
def post_job_listing():
    cursor = db.get_db().cursor()

    # Extract request data
    req_data = request.get_json()

    company_id = req_data.get('CompanyID')
    job_description = req_data.get('JobDescription')
    job_position_title = req_data.get('JobPositionTitle')

    # Validate required fields
    if not all([company_id, job_description, job_position_title]):
        return make_response(
            jsonify({"error": "Missing required fields: CompanyID, JobDescription, JobPositionTitle"}), 400
        )

    # SQL query to insert the job listing
    query = '''
        INSERT INTO JobListing (CompanyID, JobDescription, JobPositionTitle, JobIsActive)
        VALUES (%s, %s, %s, %s)
    '''

    try:
        # Execute the query, setting JobIsActive to True by default
        cursor.execute(query, (company_id, job_description, job_position_title, True))
        db.get_db().commit()
        return make_response(
            jsonify({"message": "Job listing successfully created and set as active!"}), 201
        )
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({"error": "Failed to create job listing", "details": str(e)}), 500
        )

# Update a job listing based on JobListingID 
@hiring_manager.route('/job-listings/<int:id>', methods=['PUT'])
def update_job_listing(id):
    data = request.json
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    is_active = data.get('is_active')

    # Input validation
    if not all([job_title, job_description, is_active is not None]):
        return make_response(
            jsonify({"error": "Missing required fields: job_title, job_description, is_active"}), 400
        )
    
    if not isinstance(is_active, bool):
        return make_response(
            jsonify({"error": "is_active must be a boolean value (true/false)"}), 400
        )

    query = '''
        UPDATE JobListing 
        SET JobPositionTitle = %s, JobDescription = %s, JobIsActive = %s
        WHERE JobListingID = %s
    '''

    cursor = db.get_db().cursor()
    try:
        cursor.execute(query, (job_title, job_description, is_active, id))
        db.get_db().commit()

        # Check if any rows were updated
        if cursor.rowcount == 0:
            return make_response(
                jsonify({"error": f"No job listing found with JobListingID {id}"}), 404
            )

        return make_response(
            jsonify({"message": "Job listing updated successfully"}), 200
        )
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({"error": "Failed to update job listing", "details": str(e)}), 500
        )

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