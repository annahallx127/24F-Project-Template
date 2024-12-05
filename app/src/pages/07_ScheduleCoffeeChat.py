import streamlit as st
import requests

st.title("Schedule a Coffee Chat")

mentor_id = st.text_input("Mentor ID")
mentee_id = st.text_input("Mentee ID")
availability_id = st.text_input("Availability ID")
appointment_date = st.date_input("Appointment Date")
duration = st.number_input("Duration (in minutes)", min_value=1)
meeting_subject = st.text_input("Meeting Subject")

if st.button("Schedule Coffee Chat"):
    if mentor_id and mentee_id and availability_id and appointment_date and duration and meeting_subject:
        payload = {
            "MentorID": mentor_id,
            "MenteeID": mentee_id,
            "AvailabilityID": availability_id,
            "AppointmentDate": str(appointment_date),
            "Duration": duration,
            "MeetingSubject": meeting_subject,
        }
        response = requests.post("http://localhost:8501/coffee-chat", json=payload)
        if response.status_code == 201:
            st.success("Coffee chat scheduled successfully!")
        else:
            st.error("Failed to schedule coffee chat.")
    else:
        st.warning("Please fill out all required fields.")
