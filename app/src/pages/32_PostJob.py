import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set up logging for debugging
logger = logging.getLogger(__name__)

# Configure the page layout
st.set_page_config(layout="wide")

# Add sidebar navigation
SideBarLinks()

# Title for the page
st.title("Job Listing Management")

# Section: View All Job Listings
st.header("View All Job Listings")
if st.button("Fetch Job Listings"):
    try:
        response = requests.get("http://localhost:8501/job-listings")  # Replace with your actual API URL
        if response.status_code == 200:
            job_listings = response.json()
            if job_listings:
                # Convert the data to a Pandas DataFrame for better display
                df = pd.DataFrame(job_listings)
                st.table(df)
            else:
                st.warning("No job listings available.")
        else:
            st.error("Failed to fetch job listings.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching job listings: {e}")

# Section: Add New Job Listing
st.header("Add a New Job Listing")
company_id = st.text_input("Company ID", key="company_id")
job_title = st.text_input("Job Title", key="job_title")
job_description = st.text_area("Job Description", key="job_description")

if st.button("Add Job Listing"):
    if company_id and job_title and job_description:
        payload = {
            "CompanyID": company_id,
            "JobPositionTitle": job_title,
            "JobDescription": job_description
        }
        try:
            response = requests.post("http://localhost:4000/job-listings", json=payload)
            if response.status_code == 201:
                st.success("Job listing added successfully!")
            else:
                st.error("Failed to add job listing.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error adding job listing: {e}")
    else:
        st.warning("Please fill out all fields.")

# Section: Update Existing Job Listing
st.header("Update Existing Job Listing")
job_id = st.text_input("Job ID to Update", key="job_id")
updated_title = st.text_input("Updated Job Title", key="updated_title")
updated_description = st.text_area("Updated Job Description", key="updated_description")
is_active = st.checkbox("Is Active?", value=True, key="is_active")

if st.button("Update Job Listing"):
    if job_id and updated_title and updated_description:
        payload = {
            "job_title": updated_title,
            "job_description": updated_description,
            "is_active": is_active
        }
        try:
            response = requests.put(f"http://localhost:4000/job-listings/{job_id}", json=payload)
            if response.status_code == 200:
                st.success("Job listing updated successfully!")
            else:
                st.error("Failed to update job listing.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error updating job listing: {e}")
    else:
        st.warning("Please fill out all fields.")

# Section: Delete a Job Listing
st.header("Delete a Job Listing")
delete_job_id = st.text_input("Job ID to Delete", key="delete_job_id")

if st.button("Delete Job Listing"):
    if delete_job_id:
        try:
            response = requests.delete(f"http://localhost:4000/job-listings/{delete_job_id}")
            if response.status_code == 200:
                st.success("Job listing deleted successfully!")
            else:
                st.error("Failed to delete job listing.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting job listing: {e}")
    else:
        st.warning("Please provide a Job ID.")
