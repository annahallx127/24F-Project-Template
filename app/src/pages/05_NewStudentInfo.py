import streamlit as st
import requests

st.title("Update New Student Information")

student_id = st.text_input("Student ID")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
major = st.text_input("Major")
is_mentor = st.checkbox("Is Mentor", value=False)
wcfi = st.text_input("WCFI")

if st.button("Update Student Information"):
    if student_id:
        payload = {
            "StudentID": student_id,
            "FirstName": first_name,
            "LastName": last_name,
            "Major": major,
            "isMentor": is_mentor,
            "WCFI": wcfi,
        }
        response = requests.put("http://localhost:8501/students/new_student", json=payload)
        if response.status_code == 200:
            st.success("Student information updated successfully!")
        else:
            st.error("Failed to update student information.")
    else:
        st.warning("Please provide a valid Student ID.")
