import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks


SideBarLinks(show_home=True)

# Page title
st.title("Manage Your Co-op Reviews")

# Section: Display Co-ops the student has completed
st.header("Completed Co-ops")

if st.button("Fetch Completed Co-ops"):
# Fetch completed co-ops
    url_completed_coops = f"http://web-api:4000/rs/completed_coops"
    try:
        response = requests.get(url_completed_coops)
        if response.status_code == 200:
            completed_coops = response.json()
            st.dataframe(completed_coops)
            if completed_coops:
                st.write("Here are your completed co-ops:")
                for coop in completed_coops:
                    st.write(f"**Co-op ID:** {coop['CoopID']}")
                    st.write(f"**Job Title:** {coop['JobTitle']}")
                    st.write(f"**Start Date:** {coop['StartDate']}")
                    st.write(f"**End Date:** {coop['EndDate']}")
                    st.write(f"**Company:** {coop['CompanyName']}")
                    st.write("---")
                st.write("Would you like to post a review about any of them?")
            else:
                st.info("No completed co-ops found.")
        else:
            st.error(f"Failed to fetch completed co-ops: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching completed co-ops: {e}")

# Section: Post Co-op Review
st.header("Post your co-op review")

# Input fields for Co-op review
coop_id = st.text_input("Enter the Co-op ID:", key="post_coop_id")
coop_review = st.text_area("Write your co-op review:", key="post_coop_review")
coop_rating = st.slider("Rate your co-op experience (1-5):", min_value=1, max_value=5, step=1, key="post_coop_rating")

if st.button("Submit Review"):
    if coop_id and coop_review and coop_rating:
        try:
            # Prepare the payload
            payload = {
                "CoopID": coop_id,
                "StudentID": 2,  # Hardcoded for StudentID = 2
                "CoopReview": coop_review,
                "CoopRating": coop_rating
            }

            # URL for the POST route
            url = "http://web-api:4000/rs/coop-review"

            # Send the POST request
            response = requests.post(url, json=payload)

            # Handle the response
            if response.status_code == 200:
                st.success("Co-op review posted successfully!")
            elif response.status_code == 403:
                st.warning("Unauthorized: You can only post a review for your co-ops.")
            elif response.status_code == 400:
                st.error("Invalid input. Please fill out all fields.")
            else:
                st.error(f"Failed to post review: {response.status_code}")
                st.error(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error posting review: {e}")
    else:
        st.warning("Please fill out all fields.")


st.header("Delete Your Co-op Review")

# Input fields for CoopID
coop_id = st.text_input("Enter the Co-op ID for the review you want to delete:", key="delete_coop_id")

if st.button("Delete Co-op Review"):
    if coop_id:
        try:
            # Prepare the payload
            payload = {"CoopID": coop_id}

            # URL for the DELETE route
            url = "http://web-api:4000/rs/coop-review"

            # Send the DELETE request
            response = requests.delete(url, json=payload)

            # Handle the response
            if response.status_code == 200:
                st.success("Co-op review deleted successfully!")
            elif response.status_code == 404:
                st.warning("Review not found or unauthorized.")
            elif response.status_code == 400:
                st.error("Invalid input. Please provide a valid Co-op ID.")
            else:
                st.error(f"Failed to delete review: {response.status_code}")
                st.error(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting review: {e}")
    else:
        st.warning("Please enter a valid Co-op ID.")