import pandas as pd
import streamlit as st
import requests

from modules.nav import SideBarLinks

st.title("Users Management")

SideBarLinks(show_home=True)

# Section: Retrieve Users
st.header("Retrieve Users")
user_type_filter = st.selectbox("Filter by User Type", ["All", "Student", "Employer", "Admin"], key="user_type_filter")
if st.button("Fetch Users"):
    # Define parameters for the API request
    params = {"type": user_type_filter if user_type_filter != "All" else None}
    response = requests.get("http://web-api:4000/a/users", params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            st.dataframe(pd.DataFrame(data)) 
        else:
            st.info("No users found.")
    else:
        st.error("Failed to fetch users.")

# Section: Delete User
st.header("Delete User Account")
delete_user_id = st.text_input("User ID to Delete", key="delete_user_id")
delete_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="delete_user_type")
if st.button("Delete User"):
    if delete_user_id:
        params = {"id": delete_user_id, "user_type": delete_user_type}
        response = requests.delete("http://web-api:4000/a/users", params=params)
        if response.status_code == 200:
            st.success("User deleted successfully!")
        else:
            st.error("Failed to delete user.")
    else:
        st.warning("Please enter a User ID.")

        st.title("Permissions Management")

# Section: Retrieve Current Permissions
st.header("Retrieve Current User Permissions and Roles")
if st.button("Fetch Permissions"):
    response = requests.get("http://web-api:4000/a/permissions")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch permissions.")

# Section: Update Permissions
st.header("Update Permissions for Existing Users or Roles")
update_user_id = st.text_input("User ID to Update", key="update_user_id")
update_access_level = st.text_input("New Access Level", key="update_access_level")
update_description = st.text_area("New Description", key="update_description")
update_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="update_user_type")
if st.button("Update Permissions"):
    if update_user_id and update_access_level and update_description:
        payload = {
            "user_id": update_user_id,
            "access_level": update_access_level,
            "description": update_description,
            "user_type": update_user_type
        }
        response = requests.put("http://web-api:4000/a/permissions", json=payload)
        if response.status_code == 200:
            st.success("Permissions updated successfully!")
        else:
            st.error("Failed to update permissions.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Revoke Permissions
st.header("Revoke Permissions from a User")
revoke_user_id = st.text_input("User ID to Revoke", key="revoke_user_id")
revoke_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="revoke_user_type")
if st.button("Revoke Permissions"):
    if revoke_user_id:
        params = {
            "user_id": revoke_user_id,
            "user_type": revoke_user_type
        }
        response = requests.delete("http://web-api:4000/a/permissions", params=params)
        if response.status_code == 200:
            st.success("Permissions revoked successfully!")
        else:
            st.error("Failed to revoke permissions.")
    else:
        st.warning("Please enter a User ID.")

