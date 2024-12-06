import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks  # Custom navigation component (if used)
import requests


st.set_page_config(layout="wide")

SideBarLinks()
BASE_API_URL = "http://web-api:4000"

st.title("Mary Jane's Dashboard")

# Button to view and manage availability
if st.button("Manage Availability", 
             type="primary", 
             use_container_width=True):
    st.switch_page("pages/27_availability.py")  # Link to the availability management page

# Button to view and update co-op reviews
if st.button("Manage Co-op Reviews", 
             type="primary", 
             use_container_width=True):
    st.switch_page("pages/28_coop_reviews.py")  # Link to the co-op reviews management page

# Button to view career projections
if st.button("View Career Projections", 
             type="primary", 
             use_container_width=True):
    st.switch_page("pages/29_career_projections.py")  # Link to the career projections page


