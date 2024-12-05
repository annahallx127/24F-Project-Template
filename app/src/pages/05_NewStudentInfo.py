import streamlit as st
import requests

st.title("Student Information Management")

# Section: Get Student Details
st.header("View Student Details")
student_id_detail = st.text_input("Enter Student ID to Fetch Details", key="student_id_detail")
if st.button("Fetch Student Details"):
    if student_id_detail:
        response = requests.get(f"http://localhost:8501/students/new_student/{student_id_detail}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Failed to fetch student details.")
    else:
        st.warning("Please enter a Student ID.")

# Section: Update Student Information
st.header("Update Student Information")
update_student_id = st.text_input("Student ID", key="update_student_id")
update_first_name = st.text_input("First Name", key="update_first_name")
update_last_name = st.text_input("Last Name", key="update_last_name")
update_major = st.text_input("Major", key="update_major")
update_is_mentor = st.checkbox("Is Mentor", value=False, key="update_is_mentor")
update_wcfi = st.text_input("WCFI", key="update_wcfi")
if st.button("Update Student Information"):
    if update_student_id:
        payload = {
            "StudentID": update_student_id,
            "FirstName": update_first_name,
            "LastName": update_last_name,
            "Major": update_major,
            "isMentor": update_is_mentor,
            "WCFI": update_wcfi,
        }
        update_response = requests.put("http://localhost:8501/students/new_student", json=payload)
        if update_response.status_code == 200:
            st.success("Student information updated successfully!")
        else:
            st.error("Failed to update student information.")
    else:
        st.warning("Please provide a valid Student ID.")