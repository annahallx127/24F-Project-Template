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


# # Section: Update a Review
# st.header("Update Your Co-op Review")
# st.write("Here are your existing reviews:")
# url_reviews = f"http://web-api:4000/rs/coop-review/<int:coop_id>"
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

# # Section: Delete a Review
# st.header("Delete Your Co-op Review")
# delete_review_id = st.text_input("Enter the co-op ID of the co-op review that you want to delete, you can only delete ones that you have written.", key="delete_review_id")

# if st.button("Delete Review"):
#     if delete_review_id:
#         url_delete_review = f"http://web-api:4000/rs/coop-review/{coop_id}"
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
