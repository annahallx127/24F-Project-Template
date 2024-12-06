import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests


st.title("Student Information Management")

# Section: Get Student Details
st.header("View Student Details")
student_id_detail = st.text_input("Enter Student ID to Fetch Details", key="student_id_detail")

if st.button("Fetch Student Details"):
    if student_id_detail:
        # Call the Flask API to get student details
        url = f"http://web-api:4000/students/new_student/{student_id_detail}"

        try:
            response = requests.get(url)
            st.write(response)
            if response.status_code == 200:
                student_data = response.json()
                st.write(student_data)
                st.json(student_data)  # Display the student data in JSON format
            else:
                st.error("No student found with this ID.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching student details: {e}")
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
        success = update_new_student(
            update_student_id,
            update_first_name,
            update_last_name,
            update_major,
            update_is_mentor,
            update_wcfi
        )
        if success:
            st.success("Student information updated successfully!")
        else:
            st.error("Failed to update student information or Student ID not found.")
    else:
        st.warning("Please provide a valid Student ID.")