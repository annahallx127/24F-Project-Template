import streamlit as st
import requests

st.title("Job Listings Management")

# Section: Retrieve Job Listing Details
st.header("Retrieve Job Listing Details")
job_id_get = st.text_input("Enter Job Listing ID", key="get_job_id")
if st.button("Fetch Job Details"):
    if job_id_get:
        response = requests.get(f"http://localhost:8501/job-listings/{job_id_get}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Failed to fetch job details.")
    else:
        st.warning("Please enter a Job Listing ID.")

# Section: Create Job Listing
st.header("Create Job Listing")
job_title = st.text_input("Job Title", key="create_job_title")
job_description = st.text_area("Job Description", key="create_job_description")
company_id = st.text_input("Company ID", key="create_company_id")
is_active = st.checkbox("Is Active", value=True, key="create_is_active")
if st.button("Create Job Listing"):
    if job_title and job_description and company_id:
        payload = {
            "job_title": job_title,
            "job_description": job_description,
            "company_id": company_id,
            "is_active": is_active
        }
        response = requests.post("http://localhost:8501/job-listings", json=payload)
        if response.status_code == 201:
            st.success("Job listing created successfully!")
        else:
            st.error("Failed to create job listing.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Update Job Listing
st.header("Update Job Listing")
job_id_put = st.text_input("Enter Job Listing ID to Update", key="update_job_id")
job_title_put = st.text_input("New Job Title", key="update_job_title")
job_description_put = st.text_area("New Job Description", key="update_job_description")
is_active_put = st.checkbox("Is Active", value=True, key="update_is_active")
if st.button("Update Job Listing"):
    if job_id_put:
        payload = {
            "job_title": job_title_put,
            "job_description": job_description_put,
            "is_active": is_active_put
        }
        response = requests.put(f"http://localhost:8501/job-listings/{job_id_put}", json=payload)
        if response.status_code == 200:
            st.success("Job listing updated successfully!")
        else:
            st.error("Failed to update job listing.")
    else:
        st.warning("Please enter a Job Listing ID.")

# Section: Delete Job Listing
st.header("Delete Job Listing")
job_id_delete = st.text_input("Enter Job Listing ID to Delete", key="delete_job_id")
if st.button("Delete Job Listing"):
    if job_id_delete:
        response = requests.delete(f"http://localhost:8501/job-listings/{job_id_delete}")
        if response.status_code == 200:
            st.success("Job listing deleted successfully!")
        else:
            st.error("Failed to delete job listing.")
    else:
        st.warning("Please enter a Job Listing ID.")
