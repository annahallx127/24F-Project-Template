import streamlit as st
import requests

st.title("View Job Listing Details")

job_id = st.text_input("Enter Job Listing ID")

if st.button("Fetch Job Listing Details"):
    if job_id:
        response = requests.get(f"http://localhost:8501/job-listings/{job_id}")
        if response.status_code == 200:
            job_details = response.json()
            st.json(job_details)

            # Show Schedule Coffee Chat Section only if job details are valid
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
            st.error("Failed to fetch job listing details.")
    else:
        st.warning("Please enter a Job Listing ID.")
