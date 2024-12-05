import streamlit as st
import requests

st.title("Users Management")

# Section: Retrieve Users
st.header("Retrieve Users")
user_type_filter = st.selectbox("Filter by User Type", ["All", "Student", "Employer", "Admin"], key="user_type_filter")
if st.button("Fetch Users"):
    params = {"type": None if user_type_filter == "All" else user_type_filter}
    response = requests.get("http://localhost:8501/users", params=params)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch users.")

# Section: Register a New User
st.header("Register a New User")
new_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="new_user_type")
new_user_id = st.text_input("User ID", key="new_user_id")
new_first_name = st.text_input("First Name", key="new_first_name")
new_last_name = st.text_input("Last Name", key="new_last_name")

if new_user_type == "Student":
    new_major = st.text_input("Major", key="new_major")
    new_is_mentor = st.checkbox("Is Mentor", value=False, key="new_is_mentor")
    new_wcfi = st.text_input("WCFI", key="new_wcfi")
elif new_user_type == "Employer":
    new_position = st.text_input("Position", key="new_position")

if st.button("Register User"):
    if new_user_id and new_first_name and new_last_name:
        payload = {
            "user_type": new_user_type,
            "id": new_user_id,
            "first_name": new_first_name,
            "last_name": new_last_name
        }
        if new_user_type == "Student":
            payload.update({"major": new_major, "is_mentor": new_is_mentor, "wcfi": new_wcfi})
        elif new_user_type == "Employer":
            payload.update({"position": new_position})
        response = requests.post("http://localhost:8501/users", json=payload)
        if response.status_code == 201:
            st.success("User registered successfully!")
        else:
            st.error("Failed to register user.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Update User Profile
st.header("Update User Profile")
update_user_type = st.selectbox("User Type to Update", ["Student", "Employer", "Admin"], key="update_user_type")
update_user_id = st.text_input("User ID to Update", key="update_user_id")
update_first_name = st.text_input("New First Name", key="update_first_name")
update_last_name = st.text_input("New Last Name", key="update_last_name")

if update_user_type == "Student":
    update_major = st.text_input("New Major", key="update_major")
    update_is_mentor = st.checkbox("Is Mentor", value=False, key="update_is_mentor")
    update_wcfi = st.text_input("New WCFI", key="update_wcfi")
elif update_user_type == "Employer":
    update_position = st.text_input("New Position", key="update_position")

if st.button("Update User"):
    if update_user_id and update_first_name and update_last_name:
        payload = {
            "user_type": update_user_type,
            "id": update_user_id,
            "first_name": update_first_name,
            "last_name": update_last_name
        }
        if update_user_type == "Student":
            payload.update({"major": update_major, "is_mentor": update_is_mentor, "wcfi": update_wcfi})
        elif update_user_type == "Employer":
            payload.update({"position": update_position})
        response = requests.put("http://localhost:8501/users", json=payload)
        if response.status_code == 200:
            st.success("User updated successfully!")
        else:
            st.error("Failed to update user.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Delete User
st.header("Delete User Account")
delete_user_id = st.text_input("User ID to Delete", key="delete_user_id")
delete_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="delete_user_type")
if st.button("Delete User"):
    if delete_user_id:
        params = {"id": delete_user_id, "user_type": delete_user_type}
        response = requests.delete("http://localhost:8501/users", params=params)
        if response.status_code == 200:
            st.success("User deleted successfully!")
        else:
            st.error("Failed to delete user.")
    else:
        st.warning("Please enter a User ID.")
