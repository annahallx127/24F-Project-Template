import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)


st.title("Job Listings Management")

# Section: Retrieve Job Listing Details
st.header("Retrieve Job Listing Details")
job_id_get = st.text_input("Enter Job Listing ID", key="get_job_id")
if st.button("Fetch Job Details"):
    if job_id_get:
        response = requests.get(f"http://web-api:4000/a/job-listings/{job_id_get}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Failed to fetch job details.")
    else:
        st.warning("Please enter a Job Listing ID.")

        # Section: View and Delete Expired Job Listings
st.header("Manage Expired Job Listings")
if st.button("Fetch Expired Job Listings"):
    response = requests.get("http://web-api:4000/a/job-listings/expired")
    if response.status_code == 200:
        expired_jobs = response.json()
        if expired_jobs:
            st.subheader("Expired Job Listings")
            st.json(expired_jobs)
        else:
            st.info("No expired job listings found.")
    else:
        st.error(f"Failed to fetch expired job listings: {response.status_code}")

# Section: Delete Job Listing
st.header("Delete Job Listing")
job_id_delete = st.text_input("Enter Job Listing ID to Delete", key="delete_job_id")
if st.button("Delete Job Listing"):
    if job_id_delete:
        response = requests.delete(f"http://web-api:4000/a/job-listings/{job_id_delete}")
        if response.status_code == 200:
            st.success("Job listing deleted successfully!")
        else:
            st.error("Failed to delete job listing.")
    else:
        st.warning("Please enter a Job Listing ID.")
