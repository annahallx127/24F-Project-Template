import streamlit as st
import requests

st.title("View All Job Listings")

# Fetch all job listings from the API
response = requests.get("http://web-api:4000/job-listings")
if response.status_code == 200:
    job_listings = response.json()

    if job_listings:
        # Loop through each job listing and create a clickable button for each job
        for job in job_listings:
            job_title = job["JobPositionTitle"]
            job_id = job["JobListingID"]

            # Display each job as a clickable button
            if st.button(f"View Details for {job_title}", key=f"job_{job_id}"):
                # When a job is clicked, show the details for that job
                job_details_response = requests.get(f"http://localhost:8501/job-listings/{job_id}")
                if job_details_response.status_code == 200:
                    job_details = job_details_response.json()
                    st.subheader(f"Job Details for {job_title}")
                    st.json(job_details)

                    # If the job is active, allow users to schedule a coffee chat
                    if job_details.get("JobIsActive"):
                        st.header("Schedule a Coffee Chat")
                        mentor_id = st.text_input("Mentor ID", key="mentor_id")
                        mentee_id = st.text_input("Mentee ID", key="mentee_id")
                        availability_id = st.text_input("Availability ID", key="availability_id")
                        appointment_date = st.date_input("Appointment Date", key="appointment_date")
                        duration = st.number_input("Duration (in minutes)", min_value=1, key="duration")
                        meeting_subject = st.text_input("Meeting Subject", key="meeting_subject")

                        if st.button("Schedule Coffee Chat", key="schedule_chat"):
                            if mentor_id and mentee_id and availability_id and appointment_date and duration and meeting_subject:
                                payload = {
                                    "MentorID": mentor_id,
                                    "MenteeID": mentee_id,
                                    "AvailabilityID": availability_id,
                                    "AppointmentDate": str(appointment_date),
                                    "Duration": duration,
                                    "MeetingSubject": meeting_subject,
                                }
                                chat_response = requests.post("http://localhost:8501/coffee-chat", json=payload)
                                if chat_response.status_code == 201:
                                    st.success("Coffee chat scheduled successfully!")
                                else:
                                    st.error("Failed to schedule coffee chat.")
                            else:
                                st.warning("Please fill out all required fields.")
                    else:
                        st.info("This job listing is not active. Coffee chats cannot be scheduled.")
                else:
                    st.error("Failed to fetch job details.")
    else:
        st.warning("No job listings found.")
else:
    st.error("Failed to fetch job listings.")
