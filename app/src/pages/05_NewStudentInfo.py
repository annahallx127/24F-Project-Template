import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

SideBarLinks(show_home=True)
# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = None


st.title("Student Information Management")

# Section: Get Student Details
st.header("View Student Details")
if st.button("Fetch Student Details", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':

        # Call the Flask API to get student details
        url = f"http://api:4000/ns/students/new_student"
        
        try:
            response = requests.get(url).json()
            st.session_state['student_id'] = response.get("StudentID")  # Store the StudentID
            st.write(response)
        except Exception as e:
            st.error("Failed to fetch student details.")
    else:
        st.warning("You are not logged in as Peter. Please authenticate first.")

with st.expander("What is WCFI?"):
    st.write("""
This system is a personalized tool inspired by the Myers-Briggs Type Indicator (MBTI), designed to evaluate alignment with workplace cultures. It uses four dichotomies to capture preferences in how individuals approach tasks, collaboration, competition, learning, and innovation. The result is a four-letter code that represents an individual’s work-culture fit. 

1. **Collaborative (A) vs. Independent (I):**  
   This dimension assesses whether an individual prefers working closely with others or thrives by tackling projects independently. "A" reflects a preference for teamwork and shared problem-solving, while "I" signifies a focus on autonomy and self-reliance.

2. **Competitive (E) vs. Paced (P):**  
   This axis examines motivation. "E" represents individuals who measure success by comparing themselves to others, often thriving in high-pressure, results-driven environments. On the other hand, "P" describes those who prefer a steady, self-paced approach, focusing on personal goals and avoiding external competition.

3. **Selective (S) vs. Open (O):**  
   This pair gauges attitudes toward skill development. "S" denotes a focus on mastering specific skills, favoring depth over breadth, while "O" reflects an openness to exploring diverse skills and continuous learning.

4. **Realistic (R) vs. Innovative (I):**  
   This dimension evaluates how individuals approach problem-solving and creativity. "R" indicates a practical mindset, prioritizing actionable and proven solutions, while "I" highlights a preference for visionary, experimental, and creative thinking.

By combining these attributes, this system provides insight into how individuals align with different work cultures, helping both employees and employers find environments where they can thrive. For example, an individual with the code "AIRO" may work best independently on innovative, forward-thinking projects while continuously learning.
""")
    
with st.expander("What is mine?"):
   st.write("""
The **AESI** personality type combines the attributes of being **Collaborative**, **Competitive**, **Selective**, and **Innovative**. Here’s a breakdown of what each attribute suggests and how this personality type fits into a workplace environment:

1. **Collaborative (A):**  
   Individuals with this trait thrive in team settings. They prefer working with others to achieve common goals and value shared problem-solving. In a company, they excel in roles requiring strong teamwork, such as project management, cross-functional teams, or client-facing positions. They also help foster a sense of community within the workplace.

2. **Competitive (E):**  
   The competitive nature of this personality means they are driven by comparison and metrics. They perform well in high-pressure, results-oriented environments where success is measured and rewarded, such as sales, consulting, or competitive tech sectors. This drive can inspire their team and push others to perform better, making them a valuable asset in competitive industries.

3. **Selective (S):**  
   Being selective suggests a preference for mastering specific skills rather than spreading their focus too thin. This makes them well-suited for roles that require deep expertise or specialization, such as data analysis, software development, or research-focused positions. They value honing their craft and becoming a go-to expert in their domain.

4. **Innovative (I):**  
   Innovators are forward-thinkers who prioritize creativity and visionary approaches to problem-solving. They fit best in roles or companies that encourage experimentation and bold ideas, such as startups, R&D teams, or tech innovation hubs. They bring fresh perspectives and enjoy pushing boundaries to achieve breakthroughs.

**Workplace Fit for AESI:**  
- **Ideal Roles:** Product manager, creative strategist, research scientist, or tech innovator.  
- **Team Dynamics:** They contribute significantly to brainstorming sessions and collaborative projects, blending their innovative ideas with a focus on measurable outcomes. Their selective expertise allows them to take ownership of specialized tasks while driving team success through collaborative efforts.  
- **Company Culture Fit:** AESI personalities thrive in progressive companies that reward creativity and value teamwork. They are especially well-suited to environments that emphasize innovation, continuous improvement, and competitive performance metrics. Examples include startups, creative agencies, and high-growth tech companies.

**Potential Challenges:**  
- **Overly Competitive:** Their competitive nature might cause stress or friction in overly relaxed or slow-paced environments.  
- **Preference for Mastery:** Their focus on selective skill-building could make them resistant to taking on tasks outside their area of expertise.

**Conclusion:**  
The AESI personality type is an asset to companies that value collaboration, innovation, and specialization. By leveraging their strengths and providing opportunities for both teamwork and individual mastery, organizations can help AESI individuals thrive while driving exceptional outcomes.
""") 


# Section: Update Student Information
st.header("Update Student Information")
update_major = st.text_input("Major", key="update_major")

if st.button("Update Student Information"):
    student_id = st.session_state.get("student_id")
    if student_id:
        student_info = {
            "Major": update_major
        }

        # Send the PUT request to the Flask API
        url = f"http://web-api:4000/ns/students/new_student/{student_id}"
        try:
            response = requests.put(url, json=student_info)  # Using PUT request
            if response.status_code == 200:
                st.success("Student information updated successfully!")        
            else:
                st.error(f"Failed to update student information: {response.json()['message']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error updating student information: {e}")
    else:
        st.warning("Please provide a valid Student ID.")

# Section: Get Student Details
st.header("Get All Resumes")
if st.button("Get Resumes", type='primary', use_container_width=True):
    if st.session_state.get('authenticated') and st.session_state.get('first_name') == 'Peter':

        # Call the Flask API to get student details
        url = f"http://web-api:4000/ns/resumes"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # This will be a list of resumes
                if data:
            # If the response contains data, for example, the first resume
                    student_id = data[0].get("StudentID")  # Assuming you're interested in the first resume
                    st.session_state['student_id'] = student_id
                    st.dataframe(data)  # Display the full list of resumes
                else:
                    st.warning("No resumes found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to fetch student resumes: {str(e)}")


# Section: Submit Resume
st.header("Submit Resume")
resume_name = st.text_input("Resume Name", key="resume_name")
work_experience = st.text_area("Enter Your Most Recent Work Experience", key="work_experience")
technical_skills = st.text_area("Technical Skills", key="technical_skills")
soft_skills = st.text_area("Soft Skills", key="soft_skills")


if st.button("Submit Resume", key="submit_resume"):
    if resume_name and work_experience and technical_skills and soft_skills:
        # Prepare the resume data to be sent in the request
        payload = {
            "StudentID": 1,
            "ResumeName": resume_name,
            "WorkExperience": work_experience,
            "TechnicalSkills": technical_skills,
            "SoftSkills": soft_skills,
        }

        # Step 1: Submit the resume as JSON
        response_resume = requests.post(
            "http://web-api:4000/ns/resume",
            json=payload,  # use json parameter to send JSON data
            headers={"Content-Type": "application/json"}  # Ensure correct header
        )
        
        if response_resume.status_code == 201:  # Status code 201 for successful creation
            st.success("Resume submitted successfully!")
        else:
            st.error(f"Failed to submit resume. Status Code: {response_resume.status_code}")
    else:
        st.warning("Please fill out all required fields to submit your resume.")
        
 # Section: Delete Resume
st.header("Delete Resume")
delete_resume_name = st.text_input("Enter Resume Name", key="delete_resume_student_id")
if st.button("Delete Resume"):
    if delete_resume_name:
        response = requests.delete(f"http://web-api:4000/ns/resume/{delete_resume_name}")
        if response.status_code == 200:
            st.success("Resume deleted successfully!")
        else:
            st.error("Failed to delete resume.")
    else:
        st.warning("Please enter a Resume Name.")
