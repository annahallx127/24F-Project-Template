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


st.title("Application Management")

# Section: View Applications
st.header("View Applications")
if st.button("Fetch Applications", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':
        url = (f"http://web-api:4000/ns/applications/new_student")
        try:
            response = requests.get(url).json()
            st.dataframe(response)
        except Exception as e:
            st.error("No applications found for this student.")
    else:
        st.warning(f"Failed to fetch applications.")

    

# Section: Withdraw Application
st.header("Withdraw Application")
application_id_withdraw = st.text_input("Enter Application ID to Withdraw", key="application_id_withdraw")

if st.button("Withdraw Application"):
    if application_id_withdraw:
        url = f"http://web-api:4000/ns/applications/{application_id_withdraw}/withdraw"
        response = requests.delete(url)  # Perform the DELETE request

        # Check the response status code before calling .json()
        if response.status_code == 200:
            response_data = response.json()  # Convert to dictionary if status is OK
            st.success("Application withdrawn successfully!")
        else:
            st.error("Failed to withdraw application.")
            st.write(f"Error {response.status_code}: {response.text}")
    else:
        st.warning("Please enter an Application ID.")

# Section: Update Application
st.header("Update Application")
application_id_update = st.text_input("Enter Application ID to Update", key="application_id_update")
status = st.selectbox("Status", ["Applied", "Interested", "Rejected"], key="apply_status")
update_resume_id = st.text_input("Resume ID (Optional)", key="update_resume_id")
if st.button("Update Application"):
    if application_id_update:
        payload = {
            "status": status,
            "resume_id": update_resume_id
        }
        update_response = requests.put(f"http://web-api:4000/ns/applications/{application_id_update}", json=payload)
        if update_response.status_code == 200:
            st.success("Application updated successfully!")
        else:
            st.error("Failed to update application.")
    else:
        st.warning("Please enter an Application ID.")