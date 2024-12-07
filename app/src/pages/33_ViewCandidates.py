import streamlit as st
import requests

# Set up the Streamlit page configuration
st.set_page_config(page_title="Candidate WCFI Overview", layout="wide")

# Title of the page
st.title("Candidate WCFI Overview for Job Listing")

# Input for Job ID
job_id = st.text_input("Enter Job ID")

# ------------------------------------------------------------

# Button for fetching WCFI
if st.button("Fetch Candidates' WCFI", key="fetch_wcfi"):
    with st.spinner("Fetching candidates' WCFI..."):
        # Construct the web API URL for fetching WCFI
        url = f"http://web-api:4000/hm/job-listings/{job_id}/candidates-wcfi"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                wcfi_data = response.json()
                if wcfi_data:
                    st.subheader("Candidates and WCFI")
                    st.dataframe(wcfi_data)  # Display the fetched data in a table
                else:
                    st.warning(f"No candidates found for Job ID {job_id}.")
            else:
                st.error(f"Failed to fetch WCFI. Server responded with status code {response.status_code}.")
        except Exception as e:
            st.error(f"Error occurred while fetching WCFI: {str(e)}")
