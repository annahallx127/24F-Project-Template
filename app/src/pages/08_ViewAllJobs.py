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
st.write("Enter a job id you want to hear about from a student.")
job_id = st.text_input("JobID", key="job_id")

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

st.write("Pick an availability time to book an appointment with the student.")

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

# # Fetch all job listings from the API
# response = requests.get("http://web-api:4000/ns/job-listings")
# if response.status_code == 200:
#     job_listings = response.json()

#     if job_listings:
#         # Loop through each job listing and create a clickable button for each job
#         for job in job_listings:
#             job_title = job["JobPositionTitle"]
#             job_id = job["JobListingID"]

#             # Display each job as a clickable button
#             if st.button(f"View Details for {job_title}", key=f"job_{job_id}"):
#                 # When a job is clicked, show the details for that job
#                 # try:
#                 #     job_details_response = requests.get(f"http://web-api:4000/job-listings/{job_id}").json()
#                 #     st.subheader(f"Job Details for {job_title}")
#                 #     st.write(job_details_response)
#                 # except Exception as e:
#                 #     st.error("No applications found for this student.")
#                     # If the job is active, allow users to schedule a coffee chat
#                 #     if job_details.get("JobIsActive"):
#                 #         st.header("Schedule a Coffee Chat")
#                 #         mentor_id = st.text_input("Mentor ID", key="mentor_id")
#                 #         mentee_id = st.text_input("Mentee ID", key="mentee_id")
#                 #         availability_id = st.text_input("Availability ID", key="availability_id")
#                 #         appointment_date = st.date_input("Appointment Date", key="appointment_date")
#                 #         duration = st.number_input("Duration (in minutes)", min_value=1, key="duration")
#                 #         meeting_subject = st.text_input("Meeting Subject", key="meeting_subject")

#                 #         if st.button("Schedule Coffee Chat", key="schedule_chat"):
#                 #             if mentor_id and mentee_id and availability_id and appointment_date and duration and meeting_subject:
#                 #                 payload = {
#                 #                     "MentorID": mentor_id,
#                 #                     "MenteeID": mentee_id,
#                 #                     "AvailabilityID": availability_id,
#                 #                     "AppointmentDate": str(appointment_date),
#                 #                     "Duration": duration,
#                 #                     "MeetingSubject": meeting_subject,
#                 #                 }
#                 #                 chat_response = requests.post("http://web-api:4000/coffee-chat", json=payload)
#                 #                 if chat_response.status_code == 201:
#                 #                     st.success("Coffee chat scheduled successfully!")
#                 #                 else:
#                 #                     st.error("Failed to schedule coffee chat.")
#                 #             else:
#                 #                 st.warning("Please fill out all required fields.")
#                 #     else:
#                 #         st.info("This job listing is not active. Coffee chats cannot be scheduled.")
#                 # else:
#                 #     st.error("Failed to fetch job details.")
#     else:
#         st.warning("No job listings found.")
# else:
#     st.error("Failed to fetch job listings.")
