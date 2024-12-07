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
            "Major": update_major
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

# Section: Get Student Details
st.header("Get All Resumes")
if st.button("Get Resumes", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':

        # Call the Flask API to get student details
        url = f"http://web-api:4000/ns/resumes"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # This will be a list of resumes
                if data:
            # If the response contains data, for example, the first resume
                    student_id = data[0].get("StudentID")  # Assuming you're interested in the first resume
                    st.session_state['student_id'] = student_id
                    st.dataframe(data)  # Display the full list of resumes
                else:
                    st.warning("No resumes found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to fetch student resumes: {str(e)}")


# Section: Submit Resume
st.header("Submit Resume")
resume_name = st.text_input("Resume Name", key="resume_name")
work_experience = st.text_area("Enter Your Most Recent Work Experience", key="work_experience")
technical_skills = st.text_area("Technical Skills", key="technical_skills")
soft_skills = st.text_area("Soft Skills", key="soft_skills")


if st.button("Submit Resume", key="submit_resume"):
    if resume_name and work_experience and technical_skills and soft_skills:
        # Prepare the resume data to be sent in the request
        payload = {
            "StudentID": 1,
            "ResumeName": resume_name,
            "WorkExperience": work_experience,
            "TechnicalSkills": technical_skills,
            "SoftSkills": soft_skills,
        }

        # Step 1: Submit the resume as JSON
        response_resume = requests.post(
            "http://web-api:4000/ns/resume",
            json=payload,  # use json parameter to send JSON data
            headers={"Content-Type": "application/json"}  # Ensure correct header
        )
        
        if response_resume.status_code == 201:  # Status code 201 for successful creation
            st.success("Resume submitted successfully!")
        else:
            st.error(f"Failed to submit resume. Status Code: {response_resume.status_code}")
    else:
        st.warning("Please fill out all required fields to submit your resume.")
        
 # Section: Delete Resume
st.header("Delete Resume")
delete_resume_name = st.text_input("Enter Resume Name", key="delete_resume_student_id")
if st.button("Delete Resume"):
    if delete_resume_name:
        response = requests.delete(f"http://web-api:4000/ns/resume/{delete_resume_name}")
        if response.status_code == 200:
            st.success("Resume deleted successfully!")
        else:
            st.error("Failed to delete resume.")
    else:
        st.warning("Please enter a Resume Name.")
