import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks(show_home=True)

st.title('Welcome Peter! What would you like to do?')

if st.button('Manage Student Details', 
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


