import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Configure the page layout
st.set_page_config(layout="wide")

# Add Sidebar Navigation
SideBarLinks()

# Title for the page
st.title("Manage Returning Student Availability")

# Check if the user is Mary Jane (based on session state)
if st.session_state.get('first_name') != 'Mary':
    st.error("You are not logged in as Mary Jane. Please return to the home page.")
    st.stop()

# Section: Fetch Availability
st.header("Fetch Returning Student Availability")

if st.button("Fetch Availability", type='primary', use_container_width=True):
    try:
        # Call the Flask API to get Mary Jane's availability
        url = "http://web-api:4000/rs/availabilities"  # Define the URL here
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
    except Exception as e:
        st.error(f"An error occurred while fetching availabilities: {e}")
        logger.error(f"Exception occurred: {e}")
