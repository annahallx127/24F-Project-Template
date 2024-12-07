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

SideBarLinks(show_home=True)
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
            st.session_state['student_id'] = response.get("StudentID")  # Store the StudentID
            st.write(response)
        except Exception as e:
            st.error("Failed to fetch student details.")
    else:
        st.warning("You are not logged in as Peter. Please authenticate first.")

# Section: Update Student Information
st.header("Update Student Information")
update_major = st.text_input("Major", key="update_major")

if st.button("Update Student Information"):
    student_id = st.session_state.get("student_id")
    if student_id:
        student_info = {
            "WCFI": update_wcfi
        }

        # Send the PUT request to the Flask API
        url = f"http://web-api:4000/ns/students/new_student/{student_id}"
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
