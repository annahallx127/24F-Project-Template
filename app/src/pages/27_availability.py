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

