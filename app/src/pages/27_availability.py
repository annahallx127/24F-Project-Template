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
st.header("Fetch Returning Student Availability")

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
