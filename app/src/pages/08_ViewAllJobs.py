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

st.title("View All Job Listings")

if st.button("Fetch Job Listings", key="fetch_job_listings"):
    with st.spinner("Fetching job listings..."):
        if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':
            
            url = f"http://web-api:4000/ns/job-listings"

            try:
                response = requests.get(url).json()
                st.dataframe(response)
            except Exception as e:
                st.error("No applications found for this student.")
        else:
            st.warning(f"Failed to fetch applications.")

st.header("Coffee Chat With A Student")

if st.button("Getting Available Coffee Chats", key="fetch_coffee_chat"):
    with st.spinner("Fetching coffee chats..."):
        if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':
            
            url = f"http://web-api:4000/ns/availabilities"

        response = requests.get(url)

        # Check for successful response
        if response.status_code == 200:
            availabilities = response.json()

            if availabilities:
                st.write("List of Availabilities:")
                # Display availabilities in a DataFrame table
                df = pd.DataFrame(availabilities, columns=["AvailabilityID", "StudentID", "StartDate", "EndDate"])
                st.table(df)
            else:
                st.info("No availabilities found for Mary Jane.")
        else:
            st.error(f"Failed to fetch availabilities: {response.status_code}")
            logger.error(f"Error fetching availabilities: {response.status_code}")

st.write("Pick an availability time to book an appointment with the student by inputting an availability id, the meeting subject, and the duration in minutes below.")

availability_id = st.text_input("Availability ID", key="availability_id")
meeting_subject = st.text_input("Meeting Subject", key="meeting_subject")
duration = st.text_input("Duration", key="duration")
if st.button("Book an Appointment", key="book_appointment"):
    student_id = st.session_state.get("student_id")
    with st.spinner("Fetching job listings..."):
        if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter' and availability_id and meeting_subject:
            if availability_id:
            # You can replace these values with the actual session or user-specific details
                chat_info = {
                "MenteeID": student_id,
                "AvailabilityID": availability_id,
                "Duration": duration,
                "MeetingSubject": meeting_subject
        }
            url = f"http://web-api:4000/ns/coffee-chat"

            try:
                response = requests.post(url, json=chat_info)
                st.dataframe(response)
            except Exception as e:
                st.error("Appointment cannot be made based on this availability time.")
        else:
            st.warning(f"Failed to book appointment.")

# Section: Apply for a Job
st.header("Apply for a Job")
status = st.selectbox("Status", ["Applied", "Interested", "Rejected"], key="apply_status")
job_id = st.text_input("Job ID", key="apply_job_id")

if st.button("Submit Application", key="submit_app"):
    if student_id and job_id and status:
        application_payload = {"StudentID": student_id, "JobID": job_id, "Status": status}
        response_application = requests.post("http://web-api:4000/ns/applications", json=application_payload)
        if response_application.status_code == 201:
            st.success("Application submitted successfully!")
        else:
            st.error("Failed to submit application.")
    else:
        st.warning("Please fill out all job application details.")

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
