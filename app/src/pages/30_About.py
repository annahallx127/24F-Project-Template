import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

st.write("# About Suitable")

st.markdown (
    """
    Welcome to Suitable! Suitable is created by Bella, Anna, Afra, and Isabel.
    This is an improved application of NUWorks created for a CS 3200 Course Project.  

   Suitable personalizes the job application process by addressing the challenges students, employers, and administrators face. For students, the platform offers tailored job recommendations, networking opportunities, and an application tracker. Employers benefit from automated resume ranking, collaborative hiring tools, and customized interview prompts. Administrators have advanced data security and user management features. Suitable transforms the job application process into a supportive, insightful, and secure experience, making career decisions more informed and accessible.

   With our application, we can gaurantee that as a job applicant, you'll be suited up in no time! So come along on the journey with us and stay tuned for more information and exciting features to come!
    """
        )
