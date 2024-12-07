import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks(show_home=True)

st.title('System Administrator Home Page')

if st.button('Update Job Listings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_JobListingMgmt.py')
  

if st.button('Manage All Users',
            type='primary',
            use_container_width=True):
  st.switch_page('pages/25_ManageUsers.py')

if st.button('Manage System Updates',
             type='primary',
            use_container_width=True):
  st.switch_page('pages/23_SystemUpdateMgmt.py')


if st.button('Alert System',
             type='primary',
            use_container_width=True):
  st.switch_page('pages/22_AlertSystem.py')

