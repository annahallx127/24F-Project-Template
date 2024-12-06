import streamlit as st
import requests

st.title("Users Management")

# Section: Retrieve Users
st.header("Retrieve Users")
user_type_filter = st.selectbox("Filter by User Type", ["All", "Student", "Employer", "Admin"], key="user_type_filter")
if st.button("Fetch Users"):
    params = {"type": None if user_type_filter == "All" else user_type_filter}
    response = requests.get("http://web-api:4000/users", params=params)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch users.")

# Section: Delete User
st.header("Delete User Account")
delete_user_id = st.text_input("User ID to Delete", key="delete_user_id")
delete_user_type = st.selectbox("User Type", ["Student", "Employer", "Admin"], key="delete_user_type")
if st.button("Delete User"):
    if delete_user_id:
        params = {"id": delete_user_id, "user_type": delete_user_type}
        response = requests.delete("http://web-api:4000/users", params=params)
        if response.status_code == 200:
            st.success("User deleted successfully!")
        else:
            st.error("Failed to delete user.")
    else:
        st.warning("Please enter a User ID.")
