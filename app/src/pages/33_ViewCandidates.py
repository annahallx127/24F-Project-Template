import streamlit as st
import pandas as pd
import requests

# Set up the Streamlit page configuration
st.set_page_config(page_title="Candidates Overview - SpiderVerse", layout="wide")

# Title of the page
st.title("Candidates Overview - SpiderVerse")

# Section: All Candidates' WCFI
st.header("Candidates, WCFI, and Status")

st.write("View all applicants across all job listings from SpiderVerse.")

# Button for fetching all candidates
if st.button("Fetch All Candidates", type='primary', use_container_width=True):
    with st.spinner("Fetching all candidates' WCFI and Status..."):
        # API URL for fetching all candidates
        url = f"http://web-api:4000/hm/job-listings/candidates-wcfi"  # Updated API endpoint to fetch all candidates

        try:
            # Make a GET request to the API
            response = requests.get(url)

            # Check for a successful response
            if response.status_code == 200:
                candidates = response.json()

                if candidates:
                    st.write("List of All Candidates:")
                    # Convert the JSON response to a DataFrame
                    df = pd.DataFrame(candidates, columns=["FirstName", "LastName", "Status", "WCFI"])
                    st.table(df)
                else:
                    st.info("No candidates found.")
            else:
                st.error(f"Failed to fetch candidates. Server responded with status code {response.status_code}.")
        except Exception as e:
            st.error(f"Error occurred while fetching candidates: {str(e)}")
