import streamlit as st
import pandas as pd
import requests

# Configure the Streamlit page
st.set_page_config(page_title="Candidate Rankings Overview", layout="wide")

# Title of the page
st.title("Candidate Rankings Overview")

# Section: Fetch Rankings
st.header("Candidates, WCFI, and Rankings")
st.write("View all candidates/students along with their WCFI values and rankings.")

if st.button("Fetch Rankings", type='primary', use_container_width=True):
    # API endpoint to fetch rankings
    url = "http://web-api:4000/hm/students/rankings"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            rankings = response.json()

            if rankings and isinstance(rankings, list):
                # Convert the JSON response to a DataFrame
                df = pd.DataFrame(rankings)

                # Display the rankings table
                st.write("List of All Candidates with Rankings:")
                st.table(df[["FullName", "WCFI", "Rank"]])  # Display relevant columns
            else:
                st.info("No rankings found in the database.")
        else:
            st.error(f"Failed to fetch rankings. Server responded with status code {response.status_code}.")
    except Exception as e:
        st.error(f"An error occurred while fetching rankings: {e}")
