import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Candidate WCFI Overview", layout="wide")
st.title("Candidate WCFI Overview for Job Listing")
st.header("Candidates, WCFI, and Status")

job_id = st.text_input("Enter Job ID", help="Enter the Job Listing ID to view candidate details.")

if job_id.strip():
    with st.spinner("Fetching candidates' WCFI and Status..."):
        url = f"http://web-api:4000/hm/job-listings/{job_id}/candidates-wcfi"
        try:
            response = requests.get(url)
            st.write("Raw API Response:", response.text)  # Debugging

            if response.status_code == 200:
                suitable = response.json()

                if suitable:
                    df_candidates = pd.DataFrame(suitable)
                    st.write("DataFrame Contents:", df_candidates)  # Debugging

                    required_columns = {"FirstName", "LastName", "Status", "WCFI"}
                    if required_columns.issubset(df_candidates.columns):
                        st.table(df_candidates[["FirstName", "LastName", "Status", "WCFI"]])
                    else:
                        st.error(f"Response is missing required columns: {required_columns}")
                else:
                    st.info(f"No candidates found for Job ID {job_id}.")
            else:
                st.error(f"Failed to fetch data. Server responded with status code {response.status_code}.")
        except Exception as e:
            st.error(f"Error occurred while fetching data: {str(e)}")
else:
    st.info("Please enter a Job ID to view candidates.")
