import streamlit as st
import requests
import pandas as pd

# Set up the Streamlit page configuration
st.set_page_config(page_title="Candidate Ranking", layout="wide")

# Title of the page
st.title("Candidate Rank Leaderboard")

# Input for Job ID
job_id = st.text_input("Enter JobListingID", key="job_id_input")

# Button for fetching ranked candidates
if st.button("Fetch Candidates", key="fetch_candidates"):
    if job_id.strip():  # Ensure Job ID is provided
        with st.spinner("Fetching ranked candidates..."):
            # API URL for fetching ranked candidates
            url = f"http://web-api:4000/hm/job-listings/{job_id}/rank-candidates"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    candidates_data = response.json()

                    # Display the candidates in a table format
                    if candidates_data:
                        st.subheader(f"Ranked Candidates for JobListingID = {job_id}")

                        # Convert the data to a pandas DataFrame for display
                        df = pd.DataFrame(candidates_data)

                        # Display the data with specific columns in the desired order
                        st.dataframe(df[['FirstName', 'LastName', 'WCFI', 'Status', 'RankNum']], use_container_width=True)
                    else:
                        st.warning(f"No candidates found for JobListingID {job_id}.")
                else:
                    st.error(f"Failed to fetch ranked candidates. Server responded with status code {response.status_code}.")
            except Exception as e:
                st.error(f"Error occurred while fetching ranked candidates: {str(e)}")
    else:
        st.warning("Please enter a valid JobListingID.")
