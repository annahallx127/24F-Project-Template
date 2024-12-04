import mysql.connector
from faker import Faker
import random

# Database connection function
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your server's host
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="suitable"  # Replace with your database name
        )
        print("Connection to database successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Populate the Student table
def populate_students(connection, num_rows=30):
    cursor = connection.cursor()
    fake = Faker()
    for _ in range(num_rows):
        first_name = fake.first_name()
        last_name = fake.last_name()
        major = random.choice(["Computer Science", "Mechanical Engineering", "Business"])
        is_mentor = random.choice([True, False])
        wcfi = fake.random_number(digits=4, fix_len=True)

        query = """
        INSERT INTO Student (FirstName, LastName, Major, isMentor, WCFI)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, major, is_mentor, wcfi))
    connection.commit()
    print(f"{num_rows} rows inserted into Student table.")

#Populate resumes table
def populate_resumes(connection, num_rows=30):
    cursor = connection.cursor()
    fake = Faker()

    # Get existing StudentIDs for foreign key reference
    cursor.execute("SELECT StudentID FROM Student")
    student_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        student_id = random.choice(student_ids)
        work_experience = fake.text(max_nb_chars=200)
        resume_name = fake.word() + "_resume"
        technical_skills = fake.word() + ", " + fake.word()
        soft_skills = fake.word() + ", " + fake.word()

        query = """
        INSERT INTO Resume (StudentID, WorkExperience, ResumeName, TechnicalSkills, SoftSkills)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, work_experience, resume_name, technical_skills, soft_skills))
    connection.commit()
    print(f"{num_rows} rows inserted into Resume table.")

#Populate Hiring manager
def populate_hiring_managers(connection, num_rows=15):
    cursor = connection.cursor()
    fake = Faker()

    # Get existing StudentIDs for foreign key reference
    cursor.execute("SELECT StudentID FROM Student")
    applicant_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        applicant_id = random.choice(applicant_ids)
        company_name = fake.company()
        first_name = fake.first_name()
        last_name = fake.last_name()
        position = fake.job()

        query = """
        INSERT INTO HiringManager (ApplicantID, CompanyName, FirstName, LastName, Position)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (applicant_id, company_name, first_name, last_name, position))
    connection.commit()
    print(f"{num_rows} rows inserted into HiringManager table.")

#Populate company table
def populate_companies(connection, num_rows=15):
    cursor = connection.cursor()
    fake = Faker()

    # Get existing EmployerIDs for foreign key reference
    cursor.execute("SELECT EmployerID FROM HiringManager")
    employer_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        employer_id = random.choice(employer_ids)
        name = fake.company()
        industry = random.choice(["Technology", "Engineering", "Business", "Healthcare"])

        query = """
        INSERT INTO Company (EmployerID, Name, Industry)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (employer_id, name, industry))
    connection.commit()
    print(f"{num_rows} rows inserted into Company table.")

#Populate application table
def populate_applications(connection, num_rows=30):
    cursor = connection.cursor()
    fake = Faker()

    # Get existing foreign keys
    cursor.execute("SELECT StudentID FROM Student")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT CompanyID FROM Company")
    company_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        student_id = random.choice(student_ids)
        company_id = random.choice(company_ids)
        applied_date = fake.date_this_year()
        status = random.choice(["Pending", "Interview Scheduled", "Rejected", "Accepted"])
        job_title = fake.job()
        job_description = fake.text(max_nb_chars=200)

        query = """
        INSERT INTO Application (StudentID, CompanyID, AppliedDate, Status, JobTitle, JobDescription)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, company_id, applied_date, status, job_title, job_description))
    connection.commit()
    print(f"{num_rows} rows inserted into Application table.")

#CareerProjections table
def populate_career_projections(connection, num_rows=40):
    cursor = connection.cursor()
    fake = Faker()

    # Fetch existing StudentIDs
    cursor.execute("SELECT StudentID FROM Student")
    student_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        student_id = random.choice(student_ids)
        education_timeline = fake.text(max_nb_chars=50)
        coop_timeline = fake.text(max_nb_chars=50)
        full_time_timeline = fake.text(max_nb_chars=50)

        query = """
        INSERT INTO CareerProjections (StudentID, EducationTimeline, CoopTimeline, FullTimeTimeline)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, education_timeline, coop_timeline, full_time_timeline))
    connection.commit()
    print(f"{num_rows} rows inserted into CareerProjections table.")

#Co-op Table
def populate_coop(connection, num_rows=40):
    cursor = connection.cursor()
    fake = Faker()

    # Fetch existing StudentIDs
    cursor.execute("SELECT StudentID FROM Student")
    student_ids = [row[0] for row in cursor.fetchall()]

    # Fetch existing Company Names
    cursor.execute("SELECT Name FROM Company")
    companies = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        student_id = random.choice(student_ids)
        start_date = fake.date_between(start_date='-3y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+6m')
        job_title = fake.job()
        company_name = random.choice(companies)
        coop_review = fake.text(max_nb_chars=100)
        coop_rating = random.randint(1, 5)

        query = """
        INSERT INTO Coop (StudentID, StartDate, EndDate, JobTitle, CompanyName, CoopReview, CoopRating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, start_date, end_date, job_title, company_name, coop_review, coop_rating))
    connection.commit()
    print(f"{num_rows} rows inserted into Coop table.")

# Availabilities Table
def populate_availabilities(connection, num_rows=50):
    cursor = connection.cursor()
    fake = Faker()

    # Fetch existing StudentIDs
    cursor.execute("SELECT StudentID FROM Student")
    student_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        student_id = random.choice(student_ids)
        start_date = fake.date_time_between(start_date='-1y', end_date='now')
        end_date = fake.date_time_between(start_date=start_date, end_date='+1d')

        query = """
        INSERT INTO Availabilities (StudentID, StartDate, EndDate)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (student_id, start_date, end_date))
    connection.commit()
    print(f"{num_rows} rows inserted into Availabilities table.")

#Appointment table
def populate_appointments(connection, num_rows=100):
    cursor = connection.cursor()
    fake = Faker()

    # Fetch existing Mentor and Mentee IDs
    cursor.execute("SELECT StudentID FROM Student WHERE isMentor = TRUE")
    mentor_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT StudentID FROM Student WHERE isMentor = FALSE")
    mentee_ids = [row[0] for row in cursor.fetchall()]

    # Fetch existing Availabilities
    cursor.execute("SELECT AvailabilityID FROM Availabilities")
    availability_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_rows):
        mentor_id = random.choice(mentor_ids)
        mentee_id = random.choice(mentee_ids)
        availability_id = random.choice(availability_ids)
        appointment_date = fake.date_time_between(start_date='-1y', end_date='now')
        duration = random.choice([30, 60, 90])
        meeting_subject = fake.sentence(nb_words=3)

        query = """
        INSERT INTO Appointment (MentorID, MenteeID, AvailabilityID, AppointmentDate, Duration, MeetingSubject)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (mentor_id, mentee_id, availability_id, appointment_date, duration, meeting_subject))
    connection.commit()
    print(f"{num_rows} rows inserted into Appointment table.")

#Joblistings table
def populate_job_listings(connection, num_rows=40):
    cursor = connection.cursor()
    fake = Faker()

    # Fetch existing Job IDs
    cursor.execute("SELECT JobID FROM Application")
    job_ids = [row[0] for row in cursor.fetchall()]

    for job_id in job_ids:
        is_expired = random.choice([True, False])

        query = """
        INSERT INTO JobListings (JobID, isExpired)
        VALUES (%s, %s)
        """
        cursor.execute(query, (job_id, is_expired))
    connection.commit()
    print(f"{len(job_ids)} rows inserted into JobListings table.")

#final call
if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        populate_students(connection)
        populate_resumes(connection)
        populate_hiring_managers(connection)
        populate_companies(connection)
        populate_applications(connection)
        populate_career_projections(connection)
        populate_coop(connection)
        populate_availabilities(connection)
        populate_appointments(connection)
        populate_job_listings(connection)
        connection.close()

#Call population functions
# Main execution function

if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        populate_students(connection)  # Add more populate functions as needed
        connection.close()
