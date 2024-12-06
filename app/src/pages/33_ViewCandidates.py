import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit page configuration
st.set_page_config(page_title="Candidate Overview", layout="wide")

# Title of the page
st.title("Candidate Overview for Job Listing")

# Input for Job ID
job_id = st.text_input("Enter Job ID")

# Function to fetch candidates for a specific job
def get_candidates(job_id):
    try:
        # Replace with your Flask API URL or endpoint
        response = requests.get(f'http://127.0.0.1:5000/job-listings/{job_id}/candidates')
        
        if response.status_code == 200:
            candidates = response.json()
            return pd.DataFrame(candidates)  # Convert JSON to DataFrame
        else:
            st.error(f"No candidates found for job ID {job_id}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching candidates: {str(e)}")
        return pd.DataFrame()

# Function to fetch MBTI distribution for a specific job
def get_mbti_distribution(job_id):
    try:
        # Replace with your Flask API URL or endpoint
        response = requests.get(f'http://127.0.0.1:5000/job-listings/{job_id}/mbti-distribution')
        
        if response.status_code == 200:
            mbti_distribution = response.json()
            return pd.DataFrame(mbti_distribution)  # Convert JSON to DataFrame
        else:
            st.error(f"Error fetching MBTI distribution for job ID {job_id}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching MBTI distribution: {str(e)}")
        return pd.DataFrame()

# Button to load candidate list and MBTI distribution
if st.button("View Candidates and MBTI Distribution"):
    if job_id:
        # Fetch candidates data and display it
        candidates_df = get_candidates(job_id)
        if not candidates_df.empty:
            st.subheader("Candidates who applied for the job")
            st.dataframe(candidates_df)  # Display candidates as a table
        
        # Fetch and display MBTI distribution
        mbti_df = get_mbti_distribution(job_id)
        if not mbti_df.empty:
            st.subheader("MBTI Distribution for Candidates")
            
            # Plot MBTI distribution using Matplotlib
            fig, ax = plt.subplots()
            ax.bar(mbti_df['MBTIResult'], mbti_df['Count'], color='skyblue')
            ax.set_xlabel('MBTI Type')
            ax.set_ylabel('Number of Candidates')
            ax.set_title('MBTI Distribution for Candidates of Job ID ' + str(job_id))
            st.pyplot(fig)
    else:
        st.error("Please enter a valid Job ID")
