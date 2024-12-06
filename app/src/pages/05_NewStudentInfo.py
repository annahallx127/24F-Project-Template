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

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = None


st.title("Student Information Management")

# Section: Get Student Details
st.header("View Student Details")
if st.button("Fetch Student Details", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':

        # Call the Flask API to get student details
        url = f"http://api:4000/ns/students/new_student"
        
        try:
            response = requests.get(url).json()
            st.write(response)
        except Exception as e:
            st.error("Failed to fetch student details.")
    else:
        st.warning("You are not logged in as Peter. Please authenticate first.")

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
        student_info = {
            "FirstName": update_first_name,
            "LastName": update_last_name,
            "Major": update_major,
            "isMentor": update_is_mentor,
            "WCFI": update_wcfi
        }

        # Send the PUT request to the Flask API
        url = f"http://web-api:4000/ns/students/new_student/{update_student_id}"
        try:
            response = requests.put(url, json=student_info)  # Using PUT request
            if response.status_code == 200:
                st.success("Student information updated successfully!")
            else:
                st.error(f"Failed to update student information: {response.json()['message']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error updating student information: {e}")
    else:
        st.warning("Please provide a valid Student ID.")
