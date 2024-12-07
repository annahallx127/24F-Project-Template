# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏡")

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🕴")



#### ------------------------ Examples for Role of new student------------------------
def NewStudentHomeNav():
    st.sidebar.page_link(
        "pages/04_New_Student.py", label="New Student Home", icon="🤓"
    )


def ManageStudentInfoNav():
    st.sidebar.page_link(
        "pages/05_NewStudentInfo.py", label="Manage New Student Info", icon="👩‍🎓"
    )


def ManageJobApplicationsNav():
    st.sidebar.page_link("pages/06_JobApplicationMgmt.py", label="Manage Job Applications", icon="🗂️")


def ViewJobsNav():
    st.sidebar.page_link("pages/08_ViewAllJobs.py", label="View All Jobs", icon="👩‍💻")



## ------------------------ Examples for Role of returning student ------------------------
def ReturningStudentHomeNav():
    st.sidebar.page_link("pages/26_ReturningStudentDashboard.py", label="Returning Student Dashboard", icon="🛜")



def ManageAvailabilityNav():
    st.sidebar.page_link(
        "pages/27_availability.py", label="Manage Availability", icon="📈"
    )


def ManageCoopNav():
    st.sidebar.page_link(
        "pages/28_coop_reviews.py", label="Manage Co-ops", icon="🌺"
    )

def ViewCareerProjNav():
    st.sidebar.page_link(
        "pages/29_career_projections.py", label="View Career Projections", icon="🌺"
    )


## ------------------------ Examples for Role of hiring manager ------------------------
def HiringManagerHomeNav():
    st.sidebar.page_link("pages/31_ManagerDashboard.py", label="Hiring Manager Dashboard", icon="🛜")



def ManageJobListingsNav():
    st.sidebar.page_link(
        "pages/32_PostJob.py", label="Manage Job Listings", icon="📈"
    )


def ManageCandidatesNav():
    st.sidebar.page_link(
        "pages/33_ViewCandidates.py", label="Manage Candidates", icon="🌺"
    )

def CandidateRankingNav():
    st.sidebar.page_link(
        "pages/34_Rank.py", label="Candidate Ranks", icon="🌺"
    )



#### ------------------------ System Admin Role ------------------------
def AdminHomePageNav():
    st.sidebar.page_link("pages/20_SystemAdmin_Home.py", label="System Admin", icon="🖥️")

def UpdateJobListingsNav():
    st.sidebar.page_link(
        "pages/21_JobListingMgmt.py", label="Update Job Listing", icon="💼"
    )


def ManageSystemUpdatesNav():
    st.sidebar.page_link("pages/23_SystemUpdateMgmt.py", label="Manage System Updates", icon="🔎")


def AlertSystemNav():
    st.sidebar.page_link("pages/22_AlertSystem.py", label="Alert System", icon="📬")

def ManageUsersNav():
    st.sidebar.page_link("pages/25_ManageUsers.py", label="Manage Users", icon="🖇️")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=1000)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "new_student":
            NewStudentHomeNav()
            ManageStudentInfoNav()
            ManageJobApplicationsNav()
            ViewJobsNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "system_administrator":
            AdminHomePageNav()
            UpdateJobListingsNav()
            ManageUsersNav()
            ManageSystemUpdatesNav()
            AlertSystemNav()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
