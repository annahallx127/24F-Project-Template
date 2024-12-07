import streamlit as st
import requests
import pandas as pd

# Page title
st.title("Manage Your Co-op Reviews")

# Section: Display Co-ops the student has completed
st.header("Completed Co-ops")

# Fetch completed co-ops
url_completed_coops = f"http://web-api:4000/rs/completed_coops"
try:
    response = requests.get(url_completed_coops)
    if response.status_code == 200:
        completed_coops = response.json()
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

# # Section: Post a Review
# st.header("Post a Co-op Review")
# coop_id = st.text_input("Enter the Co-op ID for which you'd like to post a review", key="coop_id")
# review_text = st.text_area("Write your review")
# rating = st.slider("Rate your experience (1-5)", 1, 5, 3)

# if st.button("Post Review"):
#     if coop_id and review_text and rating:
#         payload = {
#             "StudentID": student_id,
#             "CoopID": int(coop_id),
#             "CoopReview": review_text,
#             "CoopRating": rating
#         }
#         st.write("Payload to be sent:", payload)

#         # Send POST request to add the review
#         url_post_review = f"http://web-api:4000/rs/coop_reviews"
#         try:
#             response = requests.post(url_post_review, json=payload)
#             if response.status_code == 201:
#                 st.success("Co-op review posted successfully!")
#             else:
#                 st.error(f"Failed to post review: {response.status_code}")
#                 st.error(f"Response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error posting review: {e}")
#     else:
#         st.warning("Please fill out all fields.")

# # Section: Update a Review
# st.header("Update Your Co-op Review")
# st.write("Here are your existing reviews:")
# url_reviews = f"http://web-api:4000/rs/fetch_reviews/{student_id}"
# try:
#     response = requests.get(url_reviews)
#     if response.status_code == 200:
#         reviews = response.json()
#         if reviews:
#             df_reviews = pd.DataFrame(reviews)
#             st.table(df_reviews)
#         else:
#             st.info("No reviews found.")
#     else:
#         st.error(f"Failed to fetch reviews: {response.status_code}")
# except requests.exceptions.RequestException as e:
#     st.error(f"Error fetching reviews: {e}")

# # Input fields for updating a review
# review_id = st.text_input("Enter the Review ID you want to update", key="review_id")
# updated_review_text = st.text_area("Update your review", key="updated_review_text")
# updated_rating = st.slider("Update your rating (1-5)", 1, 5, 3, key="updated_rating")

# if st.button("Update Review"):
#     if review_id and updated_review_text and updated_rating:
#         payload = {
#             "CoopReview": updated_review_text,
#             "CoopRating": updated_rating
#         }
#         st.write("Payload to be sent:", payload)

#         # Send PUT request to update the review
#         url_update_review = f"http://web-api:4000/rs/coop_reviews/{review_id}"
#         try:
#             response = requests.put(url_update_review, json=payload)
#             if response.status_code == 200:
#                 st.success("Review updated successfully!")
#             else:
#                 st.error(f"Failed to update review: {response.status_code}")
#                 st.error(f"Response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error updating review: {e}")
#     else:
#         st.warning("Please fill out all fields.")

# # Section: Delete a Review
# st.header("Delete Your Co-op Review")
# delete_review_id = st.text_input("Enter the Review ID you want to delete", key="delete_review_id")

# if st.button("Delete Review"):
#     if delete_review_id:
#         url_delete_review = f"http://web-api:4000/rs/coop_reviews/{delete_review_id}"
#         try:
#             response = requests.delete(url_delete_review)
#             if response.status_code == 200:
#                 st.success("Review deleted successfully!")
#             else:
#                 st.error(f"Failed to delete review: {response.status_code}")
#                 st.error(f"Response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error deleting review: {e}")
#     else:
#         st.warning("Please enter a Review ID to delete.")
