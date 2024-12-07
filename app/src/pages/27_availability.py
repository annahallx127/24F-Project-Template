import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Configure the page layout
st.set_page_config(layout="wide")

# Add Sidebar Navigation
SideBarLinks(show_home=True)
# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = None

# Title for the page
st.title("Manage your availability")

# Section: Fetch Availability
st.header("View your availability")

if st.button("Fetch Availability", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Mary':
        # Call the Flask API to get Mary Jane's availability
        url = f"http://web-api:4000/rs/availabilities"  # Define the URL here
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


# Section: Post Availability
st.header("Add New Availability")
StartDate = st.text_input("Start time (format: YYYY-MM-DD HH:MI:SS)", key="StartDate")
EndDate = st.text_input("End time (format: YYYY-MM-DD HH:MI:SS)", key="EndDate")


if st.button("Post Availability"):
    if StartDate and EndDate:
        try:
            from datetime import datetime
            datetime.strptime(StartDate, "%Y-%m-%d %H:%M:%S")
            datetime.strptime(EndDate, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            st.error("Invalid date-time format. Please use 'YYYY-MM-DD HH:MI:SS'.")
            st.stop()

        # Prepare the payload
        payload = {
            "StudentID": 2,
            "StartDate": StartDate,
            "EndDate": EndDate
        }

        # Send the POST request to the Flask API
        url = "http://web-api:4000/rs/availabilities"
        try:
            response = requests.post(url, json=payload)  # Using POST request
            if response.status_code == 201:
                st.success("Availability posted successfully!")
            else:
                st.error(f"Failed to post availability: {response.status_code}")
                st.error(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error posting availability: {e}")
    else:
        st.warning("Please fill out all fields.")

# Section: Update Availabilty
st.header("Update your availability")
update_availabilityID = st.text_input("AvailabilityID", key="update_availabilityID")
StartDate = st.text_input("Start time in this format YYYY-MM-DD HH:MI:SS", key="updateStartTime")
EndDate = st.text_input("End time in this format YYYY-MM-DD HH:MI:SS", key="updateEndTime")

if st.button("Update Availability"):
    if update_availabilityID and StartDate and EndDate:
        if st.session_state.get('first_name') == 'Mary':
            payload = {
                "StartDate": StartDate,
                "EndDate": EndDate
            }

        # Send the PUT request to the Flask API
        url = f"http://web-api:4000/rs/availabilities/{update_availabilityID}"
        try:
            response = requests.put(url, json=payload)  # Using PUT request
            if response.status_code == 200:
                st.success("Availability updated successfully!")        
            else:
                st.error(f"Failed to update availability: {response.json()}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error updating availability: {e}")
    else:
        st.warning("Please fill out all fields.")

# Section: Delete Availability
st.header("Delete an Availability")

# Input field for AvailabilityID
availability_id = st.text_input("Enter AvailabilityID to delete", key="availability_id")

if st.button("Delete Availability"):
    if availability_id:
        # Confirm deletion
        confirm = st.checkbox("Are you sure you want to delete this availability?", key="confirm_delete")
        if not confirm:
            st.warning("Please confirm before proceeding.")
        else:
            # Send the DELETE request to the Flask API
            url = f"http://web-api:4000/rs/availabilities/{availability_id}"
            try:
                response = requests.delete(url)  # Using DELETE request
                if response.status_code == 200:
                    st.success(f"Availability with ID {availability_id} deleted successfully!")
                elif response.status_code == 404:
                    st.error(f"Failed to delete availability: {response.json()['message']}")
                else:
                    st.error(f"Failed to delete availability: {response.status_code}")
                    st.error(f"Response: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error deleting availability: {e}")
    else:
        st.warning("Please provide an AvailabilityID.")
