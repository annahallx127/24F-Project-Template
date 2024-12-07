import streamlit as st
import requests
import pandas as pd

# Set up the Streamlit page configuration
st.set_page_config(page_title="Candidate Rank Leaderboard", layout="wide")

# Title of the page
st.title("Candidate Rank Leaderboard")

# Input for Job ID
job_id = st.text_input("Enter Job ID", key="job_id_input")

# Button for fetching candidates
if st.button("Fetch Candidates", key="fetch_candidates"):
    if job_id.strip():  # Ensure Job ID is provided
        with st.spinner("Fetching candidates..."):
            # API URL for fetching candidates
            url = f"http://web-api:4000/hm/job-listings/{job_id}/rank-candidates"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    candidates_data = response.json()

                    # Display the candidates in a leaderboard format
                    if candidates_data:
                        st.subheader("Leaderboard")
                        st.write("Drag and drop to rank the candidates below:")
                        
                        # Convert the data to a pandas DataFrame for easier manipulation
                        df = pd.DataFrame(candidates_data)

                        # Check if "RankNum" exists in the data
                        if 'RankNum' not in df.columns:
                            df['RankNum'] = None  # Add a blank RankNum column if not present

                        # Sort candidates by their rank
                        df = df.sort_values(by='RankNum', ascending=True, na_position='last')

                        # Display candidates in a table
                        st.dataframe(df[['FirstName', 'LastName', 'WCFI', 'Status', 'RankNum']])

                        # Create a drag-and-drop feature for ranking (manual ranking)
                        rank_ids = st.text_area(
                            "Enter ranks in order (comma-separated Applicant IDs):",
                            value=", ".join(str(id) for id in df['StudentID']),
                            help="Input the Applicant IDs in the order you want to rank them (e.g., 1, 2, 3)."
                        )

                        # Submit button to update ranks
                        if st.button("Update Ranks", key="update_ranks"):
                            if rank_ids.strip():
                                rank_list = rank_ids.split(",")
                                payload = {
                                    "ranks": [{"ApplicantID": int(app_id.strip()), "RankNum": idx + 1} for idx, app_id in enumerate(rank_list)]
                                }

                                # Send POST request to update the ranks
                                update_url = f"http://web-api:4000/hm/job-listings/{job_id}/rank-candidates"
                                try:
                                    update_response = requests.post(update_url, json=payload)
                                    if update_response.status_code == 200:
                                        st.success("Ranks updated successfully!")
                                    else:
                                        st.error(f"Failed to update ranks. Error: {update_response.json().get('message', 'Unknown error')}")
                                except Exception as e:
                                    st.error(f"Error occurred while updating ranks: {str(e)}")
                            else:
                                st.warning("Please provide a valid ranking order.")
                    else:
                        st.warning(f"No candidates found for Job ID {job_id}.")
                else:
                    st.error(f"Failed to fetch candidates. Server responded with status code {response.status_code}.")
            except Exception as e:
                st.error(f"Error occurred while fetching candidates: {str(e)}")
    else:
        st.warning("Please enter a valid Job ID.")
