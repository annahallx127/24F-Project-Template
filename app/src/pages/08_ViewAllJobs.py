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

# Button to book an appointment
if st.button("Book an Appointment", key="book_appointment"):
    if availability_id:
        # API URL
        url = f"http://web-api:4000/ns/book-appointment/{availability_id}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                availability_details = response.json()
                st.write("Here are the details for the selected availability:")
                st.write(f"**Availability ID:** {availability_details['AvailabilityID']}")
                st.write(f"**Start Date:** {availability_details['StartDate']}")
                st.write(f"**End Date:** {availability_details['EndDate']}")
                st.write(f"**Mentor Name:** {availability_details['MentorName']}")
            else:
                st.error(f"Failed to fetch availability details: {response.status_code}")
        except Exception as e:
            st.error(f"Error fetching availability details: {e}")
    else:
        st.warning("Please enter an Availability ID.")


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

