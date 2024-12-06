import streamlit as st
import requests

st.title("Manage Applications")



# Section: Apply for a Job
st.header("Apply for a Job")
apply_student_id = st.text_input("Student ID", key="apply_student_id")
job_id = st.text_input("Job ID", key="apply_job_id")
status = st.selectbox("Status", ["Applied", "Interested", "Rejected"], key="apply_status")
if st.button("Submit Application"):
    if apply_student_id and job_id and status:
        payload = {"StudentID": apply_student_id, "JobID": job_id, "Status": status}
        response = requests.post("http://web-api:4000/applications", json=payload)
        if response.status_code == 201:
            st.success("Application submitted successfully!")
        else:
            st.error("Failed to submit application.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Submit Resume
st.header("Submit Resume")
resume_student_id = st.text_input("Student ID for Resume", key="resume_student_id")
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt", "rtf"], key="resume_file")
resume_name = st.text_input("Resume Name", key="resume_name")
work_experience = st.text_area("Work Experience", key="work_experience")
technical_skills = st.text_area("Technical Skills", key="technical_skills")
soft_skills = st.text_area("Soft Skills", key="soft_skills")
if st.button("Submit Resume"):
    if resume_student_id and resume_file:
        files = {"resume": resume_file}
        payload = {
            "ResumeName": resume_name,
            "WorkExperience": work_experience,
            "TechnicalSkills": technical_skills,
            "SoftSkills": soft_skills,
        }
        response = requests.post(f"http://web-api:4000/resume/{resume_student_id}", files=files, data=payload)
        if response.status_code == 200:
            st.success("Resume submitted successfully!")
        else:
            st.error("Failed to submit resume.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Delete Resume
st.header("Delete Resume")
delete_resume_student_id = st.text_input("Student ID for Resume Deletion", key="delete_resume_student_id")
if st.button("Delete Resume"):
    if delete_resume_student_id:
        response = requests.delete(f"http://web-api:4000/resume/{delete_resume_student_id}")
        if response.status_code == 200:
            st.success("Resume deleted successfully!")
        else:
            st.error("Failed to delete resume.")
    else:
        st.warning("Please enter a Student ID.")
