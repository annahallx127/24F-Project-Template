import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt


# Configure the Streamlit page
st.set_page_config(page_title="All Students Overview", layout="wide")

# Title of the page
st.title("All Students Overview")

# Section: Fetch All Students
st.header("View All Students")
st.write("Fetch and view all students in the database along with their WCFI values.")

if st.button("Fetch All Students", type='primary', use_container_width=True):
    # API endpoint to fetch all students
    url = "http://web-api:4000/hm/students"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            students = response.json()
            st.dataframe(students)
        else:
            st.error(f"Failed to fetch students. Server responded with status code {response.status_code}.")
    except Exception as e:
        st.error(f"An error occurred while fetching students: {e}")

# Section: Fetch All Students
st.header("View Students")
st.write("Visualize the distribution of WCFI values among students in a pie chart.")


if st.button("Fetch Students", type='primary', use_container_width=True):
    # API endpoint to fetch all students
    url = "http://web-api:4000/hm/students"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            students = response.json()

            # Convert the response into a DataFrame
            df = pd.DataFrame(students)

            # Check if required columns exist
            if not df.empty and 'WCFI' in df.columns:
                # Count the occurrences of each WCFI value
                wcfi_counts = df['WCFI'].value_counts()

                # Create a pie chart
                plt.figure(figsize=(8, 8))
                plt.pie(
                    wcfi_counts.values,
                    labels=wcfi_counts.index,
                    autopct="%1.1f%%",
                    startangle=140,
                )
                plt.title("WCFI Distribution Among Students")

                # Display the pie chart in Streamlit
                st.pyplot(plt)
            else:
                st.warning("Data missing required 'WCFI' column for visualization.")
        else:
            st.error(f"Failed to fetch students. Server responded with status code {response.status_code}.")
    except Exception as e:
        st.error(f"An error occurred while fetching students: {e}")