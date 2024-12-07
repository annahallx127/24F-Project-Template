# Fall 2024 CS 3200 WASABI Project

This repo is for our team WASABI- Afra Ankita, Bella Chin, Isabel Yeow, Anna Hall we created a data drive web application Suitable. Our mission is to create a better NUWorks for students, hiring managers, and system adminstrators. 

## Prerequisites

- A GitHub Account
- A terminal-based or GUI git client
- VSCode with the Python Plugin
- A distrobution of Python running on your laptop (Choco (for Windows), brew (for Macs), miniconda, Anaconda, etc). 

## Current Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory


### Setting Up Your Personal Repo

1. In GitHub, click the **fork** button in the upper right corner of the repo screen. 
1. When prompted, give the new repo a unique name, perhaps including your last name and the word 'personal'. 
1. Once the fork has been created, clone YOUR forked version of the repo to your computer. 
1. Set up the `.env` file in the `api` folder based on the `.env.template` file.
1. Start the docker containers. 

## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 



## Handling User Role Access and Control in the "Wasabi" Project
In the Wasabi project, we developed a dynamic system that manages role-based access for multiple user types, such as new students, mentors, hiring managers, and system administrators. Each user role interacts with unique features tailored to their responsibilities while sharing some overlapping functionality. This concept, known as Role-Based Access Control (RBAC), ensures a secure, intuitive, and personalized user experience.

Our implementation demonstrates how to integrate RBAC seamlessly within a Streamlit-powered app while managing user interactions and navigation efficiently.
Wrapping your head around this will take a little time and exploration of this code base.  Some highlights are below. 

Custom Sidebar Navigation:
The default sidebar is replaced with role-specific navigation managed via app/src/modules/nav.py.
Links are dynamically generated based on user roles.

Role Assignment:
Users select their role on the home page (app/src/Home.py), setting session variables for role, authentication, and personalization.
The app redirects users to their role-specific dashboards.
Role-Specific Pages:

Pages are categorized by role (e.g., New Students, Hiring Managers).
Each page dynamically displays relevant navigation links via the SideBarLinks function.

Tailored Features:
New Students: Schedule coffee chats, explore career projections, and submit co-op reviews.
Mentors: Manage availability and track mentee interactions.
Hiring Managers: Post job listings, rank candidates, and schedule interviews.
System Administrators: Manage roles, permissions, and system configurations.

