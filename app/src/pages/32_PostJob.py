import logging
import pandas as pd
import streamlit as st
import requests

# Set up logging for debugging
logger = logging.getLogger(__name__)

# Configure the page layout
st.set_page_config(layout="wide")

# Title for the page
st.title("Job Listing Management")

# ------------------------------------------------------------
# Section: View All Job Listings
st.header("View All Job Listings")

# Button for fetching job listings
if st.button("Fetch Job Listings", key="fetch_job_listings"):
    with st.spinner("Fetching job listings..."):
        if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Miles':
            
            url = f"http://web-api:4000/hm/job-listings"

            try:
                response = requests.get(url).json()
                st.dataframe(response)
            except Exception as e:
                st.error("No applications found for this student.")
        else:
            st.warning(f"Failed to fetch applications.")
           
          
    
# # ------------------------------------------------------------
# # Section: Add New Job Listing
# st.header("Add a New Job Listing")
# job_title = st.text_input("Job Title", key="job_title_input")
# job_description = st.text_area("Job Description", key="job_description_input")
# is_active_add = st.checkbox("Is Active?", value=True, key="is_active_checkbox_add")

# if st.button("Add Job Listing", key="add_job_listing"):
#     if job_title and job_description:
#         payload = {
#             "JobPositionTitle": job_title,
#             "JobDescription": job_description,
#             "JobIsActive": is_active_add
#         }
#         with st.spinner("Adding job listing..."):
#             try:
#                 response = requests.post("http://localhost:4000/hm/hiring-manager/job-listings", json=payload)
#                 if response.status_code == 201:
#                     st.success("Job listing added successfully!")
#                 else:
#                     error_message = response.json().get('message', 'Unknown error')
#                     st.error(f"Failed to add job listing. Error: {error_message}")
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Error adding job listing: {e}")
#     else:
#         st.warning("Please fill out all required fields.")

# # ------------------------------------------------------------
# # Section: Update Existing Job Listing
# st.header("Update Existing Job Listing")
# job_id = st.text_input("Job ID to Update", key="job_id_update_input")
# updated_title = st.text_input("Updated Job Title", key="updated_job_title_input")
# updated_description = st.text_area("Updated Job Description", key="updated_job_description_input")
# is_active_update = st.checkbox("Is Active?", value=True, key="is_active_checkbox_update")

# if st.button("Update Job Listing", key="update_job_listing"):
#     if job_id:
#         payload = {}
#         if updated_title:
#             payload["JobPositionTitle"] = updated_title
#         if updated_description:
#             payload["JobDescription"] = updated_description
#         payload["JobIsActive"] = is_active_update

#         if not payload:
#             st.warning("Please provide at least one field to update.")
#         else:
#             with st.spinner("Updating job listing..."):
#                 try:
#                     response = requests.put(f"http://localhost:4000/hm/hiring-manager/job-listings/{job_id}", json=payload)
#                     if response.status_code == 200:
#                         st.success("Job listing updated successfully!")
#                     else:
#                         error_message = response.json().get('message', 'Unknown error')
#                         st.error(f"Failed to update job listing. Error: {error_message}")
#                 except requests.exceptions.RequestException as e:
#                     st.error(f"Error updating job listing: {e}")
#     else:
#         st.warning("Please provide the Job ID.")

# # ------------------------------------------------------------
# # Section: Delete Job Listing
# st.header("Delete a Job Listing")
# job_id_to_delete = st.text_input("Job ID to Delete", key="job_id_delete_input")

# if st.button("Delete Job Listing", key="delete_job_listing"):
#     if job_id_to_delete:
#         try:
#             with st.spinner(f"Deleting job listing with ID {job_id_to_delete}..."):
#                 response = requests.delete(f"http://localhost:4000/hm/hiring-manager/job-listings/{job_id_to_delete}")
#                 if response.status_code == 200:
#                     st.success(f"Job listing with ID {job_id_to_delete} deleted successfully!")
#                 elif response.status_code == 404:
#                     st.warning(f"No job listing found with ID {job_id_to_delete}.")
#                 else:
#                     error_message = response.json().get('error', 'Unknown error')
#                     st.error(f"Failed to delete job listing. Error: {error_message}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error deleting job listing: {e}")
#     else:
#         st.warning("Please provide the Job ID.")
