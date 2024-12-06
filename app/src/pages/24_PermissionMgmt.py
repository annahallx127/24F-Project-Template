import streamlit as st
import requests

SideBarLinks()

st.title("Permissions Management")

# Section: Retrieve Current Permissions
st.header("Retrieve Current User Permissions and Roles")
if st.button("Fetch Permissions"):
    response = requests.get("http://web-api:4000/permissions")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch permissions.")

# Section: Assign Permissions
st.header("Assign Permissions to a New User Type")
user_id = st.text_input("User ID", key="assign_user_id")
access_level = st.text_input("Access Level", key="assign_access_level")
description = st.text_area("Description", key="assign_description")
user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="assign_user_type")
if st.button("Assign Permissions"):
    if user_id and access_level and description:
        payload = {
            "user_id": user_id,
            "access_level": access_level,
            "description": description,
            "user_type": user_type
        }
        response = requests.post("http://web-api:4000/permissions", json=payload)
        if response.status_code == 200:
            st.success("Permissions assigned successfully!")
        else:
            st.error("Failed to assign permissions.")
    else:
        st.warning("Please fill out all required fields.")

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
        response = requests.put("http://web-api:4000/permissions", json=payload)
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
        response = requests.delete("http://web-api:4000/permissions", params=params)
        if response.status_code == 200:
            st.success("Permissions revoked successfully!")
        else:
            st.error("Failed to revoke permissions.")
    else:
        st.warning("Please enter a User ID.")
