from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint for system administration routes
admin = Blueprint('admin', __name__)

#------------------------------------------------------------
# /permissions routes

# Retrieve current user permissions and roles
@admin.route('/permissions', methods=['GET'])
def get_permissions():
    query = '''
        SELECT sp.StudentID, sp.AccessLevel, sp.AccessDescription
        FROM StudentPermissions sp
        UNION ALL
        SELECT ep.EmployerID, ep.AccessLevel, ep.AccessDescription
        FROM EmployerPermissions ep
        UNION ALL
        SELECT ap.AdminID, ap.AccessLevel, ap.AccessDescription
        FROM AdminPermissions ap
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# Assign permissions to a new user type
@admin.route('/permissions', methods=['POST'])
def assign_permissions():
    data = request.json
    access_level = data['access_level']
    description = data['description']
    user_type = data['user_type']
    if user_type == 'Student':
        query = 'INSERT INTO StudentPermissions (StudentID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
    elif user_type == 'Employer':
        query = 'INSERT INTO EmployerPermissions (EmployerID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
    else:
        query = 'INSERT INTO AdminPermissions (AdminID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['user_id'], access_level, description))
    db.get_db().commit()
    return make_response("Permissions assigned successfully", 200)

# Update permissions for existing users or roles
@admin.route('/permissions', methods=['PUT'])
def update_permissions():
    data = request.json
    user_id = data['user_id']
    access_level = data['access_level']
    description = data['description']
    user_type = data['user_type']
    if user_type == 'Student':
        query = 'UPDATE StudentPermissions SET AccessLevel = %s, AccessDescription = %s WHERE StudentID = %s'
    elif user_type == 'Employer':
        query = 'UPDATE EmployerPermissions SET AccessLevel = %s, AccessDescription = %s WHERE EmployerID = %s'
    else:
        query = 'UPDATE AdminPermissions SET AccessLevel = %s, AccessDescription = %s WHERE AdminID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (access_level, description, user_id))
    db.get_db().commit()
    return make_response("Permissions updated successfully", 200)

# Revoke permissions from a user
@admin.route('/permissions', methods=['DELETE'])
def revoke_permissions():
    user_id = request.args.get('user_id')
    user_type = request.args.get('user_type')
    if user_type == 'Student':
        query = 'DELETE FROM StudentPermissions WHERE StudentID = %s'
    elif user_type == 'Employer':
        query = 'DELETE FROM EmployerPermissions WHERE EmployerID = %s'
    else:
        query = 'DELETE FROM AdminPermissions WHERE AdminID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    db.get_db().commit()
    return make_response("Permissions revoked successfully", 200)

#------------------------------------------------------------
# /system-update routes

# Retrieve current system status
@admin.route('/system-update', methods=['GET'])
def get_system_status():
    query = '''
        SELECT su.UpdateID, su.UpdateType, su.UpdateDate, su.Description, sa.FirstName, sa.LastName
        FROM SystemUpdate su
        JOIN SystemsAdministrator sa ON su.AdminID = sa.AdminID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# Submit a report or notification about a system event or issue
@admin.route('/system-update', methods=['POST'])
def submit_system_report():
    data = request.json
    update_type = data['update_type']
    description = data['description']
    admin_id = data['admin_id']
    query = 'INSERT INTO SystemUpdate (UpdateType, AdminID, UpdateDate, Description) VALUES (%s, %s, NOW(), %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (update_type, admin_id, description))
    db.get_db().commit()
    return make_response("System event submitted successfully", 200)

# Update system health monitoring configurations or thresholds
@admin.route('/system-update', methods=['PUT'])
def update_health_config():
    data = request.json
    update_id = data['update_id']
    description = data['description']
    query = 'UPDATE SystemUpdate SET Description = %s WHERE UpdateID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (description, update_id))
    db.get_db().commit()
    return make_response("System monitoring configuration updated", 200)

# Clear outdated or irrelevant system logs
@admin.route('/system-update/logs', methods=['DELETE'])
def clear_logs():
    query = 'DELETE FROM DataArchive WHERE ArchiveDate < NOW() - INTERVAL 127 DAY'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Outdated logs cleared", 200)

#------------------------------------------------------------
# /alert-system routes

# Retrieve audit logs of user actions and system changes
@admin.route('/alert-system/audit-logs', methods=['GET'])
def get_audit_logs():
    query = '''
        SELECT a.AlertID, a.ActivityType, a.Description, a.Severity, a.Timestamp, a.Status,
               CASE 
                   WHEN a.GeneratedBy IN (SELECT StudentID FROM Student) THEN 'Student'
                   WHEN a.GeneratedBy IN (SELECT EmployerID FROM HiringManager) THEN 'Employer'
                   WHEN a.GeneratedBy IN (SELECT AdminID FROM SystemsAdministrator) THEN 'Admin'
               END AS GeneratedByType
        FROM AlertSystem a
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# Submit new alerts or event flags
@admin.route('/alert-system', methods=['POST'])
def submit_alert():
    data = request.json
    activity_type = data['activity_type']
    description = data['description']
    severity = data['severity']
    generated_by = data['generated_by']
    query = 'INSERT INTO AlertSystem (ActivityType, Description, Severity, Timestamp, GeneratedBy) VALUES (%s, %s, %s, NOW(), %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (activity_type, description, severity, generated_by))
    db.get_db().commit()
    return make_response("Alert submitted successfully", 200)

# Update alert configurations or mark specific alerts as resolved
@admin.route('/alert-system', methods=['PUT'])
def update_alert_config():
    data = request.json
    alert_id = data['alert_id']
    status = data['status']
    query = 'UPDATE AlertSystem SET Status = %s WHERE AlertID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (status, alert_id))
    db.get_db().commit()
    return make_response("Alert updated successfully", 200)

# Delete logs older than the retention policy
@admin.route('/alert-system/logs', methods=['DELETE'])
def delete_old_logs():
    query = 'DELETE FROM AlertSystem WHERE Timestamp < NOW() - INTERVAL 90 DAY'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Old logs deleted", 200)

#------------------------------------------------------------
# /job-listings routes

#------------------------------------------------------------
# Get all expired job listings
@admin.route('/job-listings/expired', methods=['GET'])
def get_expired_job_listings():
    current_app.logger.info('GET /job-listings/expired route')

    # Get the current date and time to compare with job expiry date
    from datetime import datetime
    current_time = datetime.now()

    # Query to fetch job listings where the expiration date (isActive) is less than the current time
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT JobListingID, JobPositionTitle, JobDescription, isActive
        FROM JobListings
        WHERE isActive = False
    """)

    expired_jobs = cursor.fetchall()

    # Check if there are any expired job listings
    if expired_jobs:
        the_response = make_response(jsonify(expired_jobs))
        the_response.status_code = 200
        return the_response
    else:
        return jsonify({'message': 'No expired job listings found'}), 404

# Retrieve detailed information about a specific job posting
@admin.route('/job-listings/<id>', methods=['GET'])
def get_job_details(id):
    query = '''
        SELECT jl.JobListingID, jl.JobPositionTitle, jl.JobDescription, jl.JobIsActive, 
               c.Name AS CompanyName, c.Industry,
               hm.FirstName AS HiringManagerFirstName, hm.LastName AS HiringManagerLastName
        FROM JobListing jl
        JOIN Company c ON jl.CompanyID = c.CompanyID
        JOIN HiringManager hm ON c.EmployerID = hm.EmployerID
        WHERE jl.JobListingID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (id,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# Create a new job listing
@admin.route('/job-listings', methods=['POST'])
def create_job_listing():
    data = request.json
    job_title = data['job_title']
    job_description = data['job_description']
    company_id = data['company_id']
    is_active = data['is_active']
    query = '''
        INSERT INTO JobListing (JobPositionTitle, JobDescription, CompanyID, JobIsActive)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (job_title, job_description, company_id, is_active))
    db.get_db().commit()
    return make_response("Job listing created successfully", 201)

# Update a job listing
@admin.route('/job-listings/<id>', methods=['PUT'])
def update_job_listing(id):
    data = request.json
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    is_active = data.get('is_active')
    query = '''
        UPDATE JobListing 
        SET JobPositionTitle = %s, JobDescription = %s, JobIsActive = %s
        WHERE JobListingID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (job_title, job_description, is_active, id))
    db.get_db().commit()
    return make_response("Job listing updated successfully", 200)

# Delete a job listing
@admin.route('/job-listings/<id>', methods=['DELETE'])
def delete_job_listing(id):
    query = 'DELETE FROM JobListing WHERE JobListingID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (id,))
    db.get_db().commit()
    return make_response("Job listing deleted successfully", 200)

@users.route('/users', methods=['GET'])
def get_users():
    user_type = request.args.get('type')  # Optional filter for user type
    if user_type == 'Student':
        query = 'SELECT StudentID, FirstName, LastName, Major, isMentor, WCFI FROM Student'
    elif user_type == 'Employer':
        query = 'SELECT EmployerID, FirstName, LastName, Position FROM HiringManager'
    elif user_type == 'Admin':
        query = 'SELECT AdminID, FirstName, LastName FROM SystemsAdministrator'
    else:
        # Retrieve all users by combining queries
        query = '''
            SELECT 'Student' AS UserType, StudentID AS ID, FirstName, LastName FROM Student
            UNION ALL
            SELECT 'Employer', EmployerID, FirstName, LastName FROM HiringManager
            UNION ALL
            SELECT 'Admin', AdminID, FirstName, LastName FROM SystemsAdministrator
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# Register a new user
@users.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_type = data.get('user_type')
    if user_type == 'Student':
        query = '''
            INSERT INTO Student (StudentID, FirstName, LastName, Major, isMentor, WCFI)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (data['id'], data['first_name'], data['last_name'], data['major'], data['is_mentor'], data['wcfi'])
    elif user_type == 'Employer':
        query = '''
            INSERT INTO HiringManager (EmployerID, FirstName, LastName, Position)
            VALUES (%s, %s, %s, %s)
        '''
        values = (data['id'], data['first_name'], data['last_name'], data['position'])
    elif user_type == 'Admin':
        query = '''
            INSERT INTO SystemsAdministrator (AdminID, FirstName, LastName)
            VALUES (%s, %s, %s)
        '''
        values = (data['id'], data['first_name'], data['last_name'])
    else:
        return make_response("Invalid user type", 400)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return make_response("User created successfully", 201)

# Update user profile details
@users.route('/users', methods=['PUT'])
def update_user():
    data = request.json
    user_id = data.get('id')
    user_type = data.get('user_type')
    if user_type == 'Student':
        query = '''
            UPDATE Student
            SET FirstName = %s, LastName = %s, Major = %s, isMentor = %s, WCFI = %s
            WHERE StudentID = %s
        '''
        values = (data['first_name'], data['last_name'], data['major'], data['is_mentor'], data['wcfi'], user_id)
    elif user_type == 'Employer':
        query = '''
            UPDATE HiringManager
            SET FirstName = %s, LastName = %s, Position = %s
            WHERE EmployerID = %s
        '''
        values = (data['first_name'], data['last_name'], data['position'], user_id)
    elif user_type == 'Admin':
        query = '''
            UPDATE SystemsAdministrator
            SET FirstName = %s, LastName = %s
            WHERE AdminID = %s
        '''
        values = (data['first_name'], data['last_name'], user_id)
    else:
        return make_response("Invalid user type", 400)

    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return make_response("User updated successfully", 200)

# Delete a user account
@users.route('/users', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id')
    user_type = request.args.get('user_type')
    if user_type == 'Student':
        query = 'DELETE FROM Student WHERE StudentID = %s'
    elif user_type == 'Employer':
        query = 'DELETE FROM HiringManager WHERE EmployerID = %s'
    elif user_type == 'Admin':
        query = 'DELETE FROM SystemsAdministrator WHERE AdminID = %s'
    else:
        return make_response("Invalid user type", 400)

    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    db.get_db().commit()
    return make_response("User deleted successfully", 200)