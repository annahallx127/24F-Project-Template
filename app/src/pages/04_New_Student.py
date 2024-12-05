import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('New Student Home Page')

if st.button('Update Student Details', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_NewStudentInfo.py')

if st.button('Manage Job Applications',
             type='primary',
            use_container_width=True):
  st.switch_page('pages/06_JobApplicationMgmt.py')


if st.button('View All Jobs',
             type='primary',
            use_container_width=True):
  st.switch_page('pages/08_ViewAllJobs.py')


if st.button('Apply For Jobs',
             type='primary',
            use_container_width=True):
  st.switch_page('pages/09_ApplyForJob.py')

