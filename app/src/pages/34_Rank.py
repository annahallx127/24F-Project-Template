import streamlit as st
import pandas as pd
import requests

# Configure the Streamlit page
st.set_page_config(page_title="Candidate Rankings Overview", layout="wide")

# Title of the page
st.title("Candidate Rankings Overview")

# Section: Fetch Rankings
st.header("View Candidates, WCFI, and Rankings")

if st.button("Fetch Rankings", type='primary', use_container_width=True):
    # API endpoint to fetch rankings
    url = "http://web-api:4000/students/rankings"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            rankings = response.json()
            df = pd.DataFrame(rankings)

            # Display rankings in a table
            st.write("Candidates, WCFI, and Rankings:")
            st.table(df)
        else:
            st.error(f"Failed to fetch rankings. Server responded with status code {response.status_code}.")
    except Exception as e:
        st.error(f"An error occurred while fetching rankings: {e}")
