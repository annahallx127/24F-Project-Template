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

# Section: Fetch Availability
st.header("Fetch Returning Student Availability")

if st.button("Fetch Availability", type='primary', use_container_width=True):
    try:
        # Call the Flask API to get the returning student's availability
        url = "http://web-api:4000/availabilities"
        response = requests.get(url)

        # Check for successful response
        if response.status_code == 200:
            availabilities = response.json()

            if availabilities:
                st.write("List of Availabilities:")
                # Display availabilities in a DataFrame table
                df = pd.DataFrame(availabilities, columns=["AvailabilityID", "StartDate", "EndDate"])
                st.table(df)
            else:
                st.info("No availabilities found for the returning student.")
        else:
            st.error(f"Failed to fetch availabilities: {response.status_code}")
            logger.error(f"Error fetching availabilities: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")
        logger.error(f"Exception occurred: {e}")
