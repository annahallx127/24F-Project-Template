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
    try:
        query = '''
            SELECT sp.StudentID AS UserID, sp.AccessLevel, sp.AccessDescription, 'Student' AS UserType
            FROM StudentPermissions sp
            UNION ALL
            SELECT ep.EmployerID AS UserID, ep.AccessLevel, ep.AccessDescription, 'Employer' AS UserType
            FROM EmployerPermissions ep
            UNION ALL
            SELECT ap.AdminID AS UserID, ap.AccessLevel, ap.AccessDescription, 'Admin' AS UserType
            FROM AdminPermissions ap
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)

# Assign permissions to a new user type
@admin.route('/permissions', methods=['POST'])
def assign_permissions():
    try:
        data = request.json
        access_level = data['access_level']
        description = data['description']
        user_type = data['user_type']
        if user_type == 'Student':
            query = 'INSERT INTO StudentPermissions (StudentID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
        elif user_type == 'Employer':
            query = 'INSERT INTO EmployerPermissions (EmployerID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
        elif user_type == 'Admin':
            query = 'INSERT INTO AdminPermissions (AdminID, AccessLevel, AccessDescription) VALUES (%s, %s, %s)'
        else:
            return make_response({"error": "Invalid user_type"}, 400)
        cursor = db.get_db().cursor()
        cursor.execute(query, (data['user_id'], access_level, description))
        db.get_db().commit()
        return make_response({"message": "Permissions assigned successfully"}, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)

# Update permissions for existing users or roles
@admin.route('/permissions', methods=['PUT'])
def update_permissions():
    try:
        data = request.json
        user_id = data['user_id']
        access_level = data['access_level']
        description = data['description']
        user_type = data['user_type']
        if user_type == 'Student':
            query = 'UPDATE StudentPermissions SET AccessLevel = %s, AccessDescription = %s WHERE StudentID = %s'
        elif user_type == 'Employer':
            query = 'UPDATE EmployerPermissions SET AccessLevel = %s, AccessDescription = %s WHERE EmployerID = %s'
        elif user_type == 'Admin':
            query = 'UPDATE AdminPermissions SET AccessLevel = %s, AccessDescription = %s WHERE AdminID = %s'
        else:
            return make_response({"error": "Invalid user_type"}, 400)
        cursor = db.get_db().cursor()
        cursor.execute(query, (access_level, description, user_id))
        db.get_db().commit()
        return make_response({"message": "Permissions updated successfully"}, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)

# Revoke permissions from a user
@admin.route('/permissions', methods=['DELETE'])
def revoke_permissions():
    try:
        user_id = request.args.get('user_id')
        user_type = request.args.get('user_type')
        if user_type == 'Student':
            query = 'DELETE FROM StudentPermissions WHERE StudentID = %s'
        elif user_type == 'Employer':
            query = 'DELETE FROM EmployerPermissions WHERE EmployerID = %s'
        elif user_type == 'Admin':
            query = 'DELETE FROM AdminPermissions WHERE AdminID = %s'
        else:
            return make_response({"error": "Invalid user_type"}, 400)
        cursor = db.get_db().cursor()
        cursor.execute(query, (user_id,))
        db.get_db().commit()
        return make_response({"message": "Permissions revoked successfully"}, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


