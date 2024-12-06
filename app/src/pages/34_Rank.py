import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to get rankings of candidates for a specific job
def get_candidates_ranking(job_id):
    response = requests.get(f"http://localhost:5000/job-listings/{job_id}/candidates-ranking")
    return response.json()

# Function to get all candidates rankings
def get_all_candidates_ranking():
    response = requests.get(f"http://localhost:5000/candidates-ranking")
    return response.json()

# Streamlit page for candidate rankings
st.title("Candidate Ranking for Job Listings")

# Input job ID to fetch job-specific ranking or view all candidates
job_id = st.text_input("Enter Job ID (leave blank to view all candidates)")

if job_id:
    # Fetch rankings for specific job
    rankings = get_candidates_ranking(job_id)
    if rankings:
        st.write(f"Rankings for Job ID {job_id}")
        df = pd.DataFrame(rankings)
        st.dataframe(df)

        # Display rankings as a bar chart
        fig, ax = plt.subplots()
        ax.bar(df['FirstName'] + " " + df['LastName'], df['RankNum'])
        ax.set_xlabel("Candidate Name")
        ax.set_ylabel("Ranking")
        ax.set_title(f"Ranking of Candidates for Job ID {job_id}")
        st.pyplot(fig)
    else:
        st.write(f"No rankings found for Job ID {job_id}")
else:
    # Fetch all candidates rankings
    rankings = get_all_candidates_ranking()
    if rankings:
        st.write("All Candidates Rankings")
        df = pd.DataFrame(rankings)
        st.dataframe(df)

        # Display rankings as a bar chart
        fig, ax = plt.subplots()
        ax.bar(df['FirstName'] + " " + df['LastName'], df['RankNum'])
        ax.set_xlabel("Candidate Name")
        ax.set_ylabel("Ranking")
        ax.set_title("Ranking of All Candidates")
        st.pyplot(fig)
    else:
        st.write("No candidate rankings found.")
