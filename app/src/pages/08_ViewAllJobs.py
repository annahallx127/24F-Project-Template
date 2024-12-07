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

st.write("Pick an availability time to book an appointment with the student by inputting an availability ID, the meeting subject, and the duration in minutes below.")

# Inputs
availability_id = st.text_input("Availability ID", key="availability_id")
start_date = st.text_input("StartDate", key="start_date")
meeting_subject = st.text_input("Meeting Subject", key="meeting_subject")
duration = st.text_input("Duration (in minutes)", key="duration")

# Button to book an appointment
if st.button("Book an Appointment", key="book_appointment"):
    if availability_id and meeting_subject and duration:
        try:
            # Validate duration is a number
            duration = int(duration)
        except ValueError:
            st.error("Duration must be a valid number (in minutes).")
            st.stop()

        # Hardcoded or fetched student_id
        student_id = st.session_state.get("student_id", 1)  # Default to 2 for now

        # Construct payload
        chat_info = {
            "MentorID": 1,
            "MenteeID": student_id,
            "AvailabilityID": availability_id,
            "StartDate": start_date,
            "Duration": duration,
            "MeetingSubject": meeting_subject
        }


        # API URL
        url = "http://web-api:4000/ns/coffee-chat"

        try:
            # Send POST request
            response = requests.post(url, json=chat_info)

            # Check the response status
            if response.status_code == 201:
                st.dataframe(chat_info)
                st.success("Appointment successfully booked!")
            else:
                st.error(f"Failed to book appointment: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error while booking the appointment: {e}")
    else:
        st.warning("Please fill out all fields.")

# Section: Apply for a Job
st.header("Apply for a Job")
status = st.selectbox("Status", ["Applied", "Interested", "Rejected"], key="apply_status")
job_id = st.text_input("Job ID", key="apply_job_id")

if st.button("Submit Application", key="submit_app"):
    if job_id and status:
        application_payload = {"StudentID": 1, "JobID": job_id, "Status": status}
        response_application = requests.post("http://web-api:4000/ns/applications", json=application_payload)
        if response_application.status_code == 201:
            st.success("Application submitted successfully!")
        else:
            st.error("Failed to submit application.")
    else:
        st.warning("Please fill out all job application details.")

