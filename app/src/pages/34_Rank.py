import streamlit as st
import pandas as pd
import requests

# Configure the Streamlit page
st.set_page_config(page_title="Candidate Rankings Overview", layout="wide")

# Title of the page
st.title("Candidate Rankings Overview")

# Section: View Rankings
st.header("View Candidate Rankings")
st.write("Display unique rankings of all candidates along with their details.")

# Button to fetch unique rankings with students
if st.button("Fetch Rankings", type='primary', use_container_width=True):
    # API endpoint to fetch rankings with students
    url = "http://web-api:4000/hm/students/rankings"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            rankings = response.json()

            # Convert the response to a DataFrame
            df = pd.DataFrame(rankings, columns=["StudentID", "FirstName", "LastName", "WCFI", "RankNum"])

            # Create a combined "Name" column
            df["Name"] = df["FirstName"] + " " + df["LastName"]

            # Remove duplicate RankNum entries while keeping the first occurrence
            df = df.drop_duplicates(subset=["RankNum"])

            # Display the rankings table
            st.write("Rankings of Candidates:")
            st.table(df[["RankNum", "Name", "WCFI"]])  # Display RankNum, Name, and WCFI

        elif response.status_code == 404:
            st.info("No rankings or students found.")
        else:
            st.error(f"Failed to fetch rankings. Server responded with status code {response.status_code}.")
    except Exception as e:
        st.error(f"An error occurred while fetching rankings: {e}")
