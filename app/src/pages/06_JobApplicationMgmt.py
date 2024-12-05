import streamlit as st
import requests

st.title("Update Job Applications")

application_id = st.text_input("Enter Application ID")

if st.button("Withdraw Application"):
    if application_id:
        response = requests.delete(f"http://localhost:8501/applications/{application_id}/withdraw")
        if response.status_code == 200:
            st.success("Application withdrawn successfully!")
        else:
            st.error("Failed to withdraw application.")
    else:
        st.warning("Please enter an Application ID.")

st.title("Update Application")

application_id = st.text_input("Application ID")
rank = st.number_input("Rank", min_value=0)
status = st.text_input("Status")
resume_id = st.text_input("Resume ID (Optional)")

if st.button("Update Application"):
    if application_id:
        payload = {
            "rank": rank,
            "status": status,
            "resume_id": resume_id,
        }
        response = requests.put(f"http://localhost:8501/applications/{application_id}", json=payload)
        if response.status_code == 200:
            st.success("Application updated successfully!")
        else:
            st.error("Failed to update application.")
    else:
        st.warning("Please enter an Application ID.")