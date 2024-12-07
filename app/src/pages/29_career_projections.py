import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Career Projections")

tab1, tab2, tab3 = st.tabs(["Education Timeline", "Co-op Timeline", "Full-time Work Timeline"])

with tab1:
    st.header("Education Timeline")
    st.write("Details about your education timeline go here...")

with tab2:
    st.header("Co-op Timeline")
    st.write("Details about your co-op timeline go here...")

with tab3:
    st.header("Full-time Work Timeline")
    st.write("Details about your full-time work timeline go here...")
