import streamlit as st
import requests

# Set up the page layout
st.set_page_config(layout="wide")

st.title("Manage Availability")

# Section: View Availability
st.header("View Availability")
student_id_view = st.text_input("Enter Student ID to View Availability", key="view_student_id")

if st.button("Fetch Availability"):
    if student_id_view:
        response = requests.get(f"http://localhost:8501/availability/{student_id_view}")
        if response.status_code == 200:
            availabilities = response.json()
            if availabilities:
                st.write("Your Availability:")
                for availability in availabilities:
                    st.write(f"Availability ID: {availability['AvailabilityID']}")
                    st.write(f"Start: {availability['StartDate']}")
                    st.write(f"End: {availability['EndDate']}")
                    st.write("---")
            else:
                st.info("No availability found.")
        else:
            st.error("Failed to fetch availability. Please try again.")
    else:
        st.warning("Please enter a valid Student ID.")

# Section: Add Availability
st.header("Add Availability")
student_id_add = st.text_input("Student ID", key="add_student_id")
start_date_add = st.text_input("Start Date & Time (YYYY-MM-DD HH:MM:SS)", key="add_start_date")
end_date_add = st.text_input("End Date & Time (YYYY-MM-DD HH:MM:SS)", key="add_end_date")

if st.button("Add Availability"):
    if student_id_add and start_date_add and end_date_add:
        payload = {
            "StudentID": student_id_add,
            "StartDate": start_date_add,
            "EndDate": end_date_add,
        }
        response = requests.post("http://localhost:8501/availability", json=payload)
        if response.status_code == 201:
            st.success("Availability added successfully!")
        else:
            st.error("Failed to add availability. Please try again.")
    else:
        st.warning("Please fill out all fields to add availability.")

# Section: Update Availability
st.header("Update Availability")
availability_id_update = st.text_input("Availability ID to Update", key="update_availability_id")
start_date_update = st.text_input("New Start Date & Time (YYYY-MM-DD HH:MM:SS)", key="update_start_date")
end_date_update = st.text_input("New End Date & Time (YYYY-MM-DD HH:MM:SS)", key="update_end_date")

if st.button("Update Availability"):
    if availability_id_update and start_date_update and end_date_update:
        payload = {
            "StartDate": start_date_update,
            "EndDate": end_date_update,
        }
        response = requests.put(f"http://localhost:8501/availability/{availability_id_update}", json=payload)
        if response.status_code == 200:
            st.success("Availability updated successfully!")
        else:
            st.error("Failed to update availability. Please try again.")
    else:
        st.warning("Please fill out all fields to update availability.")

# Section: Delete Availability
st.header("Delete Availability")
availability_id_delete = st.text_input("Availability ID to Delete", key="delete_availability_id")

if st.button("Delete Availability"):
    if availability_id_delete:
        response = requests.delete(f"http://localhost:8501/availability/{availability_id_delete}")
        if response.status_code == 200:
            st.success("Availability deleted successfully!")
        else:
            st.error("Failed to delete availability. Please try again.")
    else:
        st.warning("Please enter an Availability ID to delete.")
