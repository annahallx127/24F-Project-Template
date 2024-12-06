DROP DATABASE IF EXISTS suitable;

CREATE DATABASE  IF NOT EXISTS suitable;

USE suitable;

CREATE TABLE IF NOT EXISTS `Student` (
  `StudentID` integer PRIMARY KEY AUTO_INCREMENT,
  `FirstName` varchar(300) NOT NULL,
  `LastName` varchar(300) NOT NULL,
  `Major` varchar(500) NOT NULL,
  `isMentor` boolean NOT NULL,
  `WCFI` varchar(4)
);

CREATE TABLE IF NOT EXISTS `Resume` (
  `ResumeID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `WorkExperience` mediumtext,
  `ResumeName` varchar(50),
  `TechnicalSkills` varchar(100),
  `SoftSkills` varchar(100),
   FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE

);


CREATE TABLE IF NOT EXISTS `HiringManager` (
  `EmployerID` integer PRIMARY KEY AUTO_INCREMENT,
    `ApplicantID` integer NOT NULL,
  `FirstName` varchar(50),
  `LastName` varchar(50),
  `Position` varchar(100),
    FOREIGN KEY (ApplicantID) REFERENCES Student(StudentID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Company` (
  `CompanyID` integer PRIMARY KEY AUTO_INCREMENT,
    `EmployerID` integer NOT NULL,
  `Name` varchar(300),
  `Industry` varchar(100),
    FOREIGN KEY (EmployerID) REFERENCES HiringManager(EmployerID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `JobListings` (
  `JobListingID` integer PRIMARY KEY AUTO_INCREMENT,
    `CompanyID` integer NOT NULL,
    `JobDescription` mediumtext,
    `JobPositionTitle` varchar(100),
    `JobIsActive` boolean,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID) ON DELETE CASCADE
    );


CREATE TABLE IF NOT EXISTS `Application` (
  `ApplicationID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `AppliedDate` date,
  `Status` varchar(30),
  `JobID` integer NOT NULL,
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE,
      FOREIGN KEY (JobID) REFERENCES JobListings(JobListingID) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS `CareerProjections` (
  `TimelineID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `EducationTimeline` text,
  `CoopTimeline` text,
  `FullTimeTimeline` text,
FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS `Coop` (
  `CoopID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `StartDate` Date,
  `EndDate` Date,
  `JobTitle` varchar(100),
  `CompanyName` varchar(200),
  `CoopReview` mediumText,
  `CoopRating` integer,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (CoopID) REFERENCES JobListings(JobListingID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Availabilities` (
`AvailabilityID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `StartDate` datetime,
  `EndDate` datetime,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS `Appointment` (
  `AppointmentID` integer PRIMARY KEY AUTO_INCREMENT,
  `MentorID` integer NOT NULL,
  `MenteeID` integer NOT NULL,
    `AvailabilityID` integer NOT NULL,
  `AppointmentDate` datetime,
  `Duration` integer,
  `MeetingSubject` varchar(50),
  FOREIGN KEY (MentorID) REFERENCES Student(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (MenteeID) REFERENCES Student(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (AvailabilityID) REFERENCES Availabilities(AvailabilityID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS `Rank` (
  `ApplicantID` integer NOT NULL,
  `RankNum` integer,
    FOREIGN KEY (ApplicantID) REFERENCES Student(StudentID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `SystemsAdministrator` (
  `AdminID` integer PRIMARY KEY AUTO_INCREMENT,
  `FirstName` varchar(50),
  `LastName` varchar(50)
);

CREATE TABLE IF NOT EXISTS `SystemUpdate` (
  `UpdateID` integer PRIMARY KEY AUTO_INCREMENT,
  `UpdateType` varchar(100),
  `AdminID` integer NOT NULL,
  `UpdateDate` date,
  `Description` text,
    FOREIGN KEY (AdminID) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `DataArchive` (
  `UpdateID` integer PRIMARY KEY AUTO_INCREMENT,
  `DataType` varchar(100),
  `ArchiveDate` date,
  `AdminID` integer NOT NULL,
    FOREIGN KEY (UpdateID) REFERENCES SystemUpdate(UpdateID) ON DELETE CASCADE,
    FOREIGN KEY (AdminID) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `DataBackup` (
  `BackupID` integer PRIMARY KEY AUTO_INCREMENT,
  `UpdateID` integer NOT NULL,
  `BackupDate` date,
  `DataSize` integer,
    FOREIGN KEY (UpdateID) REFERENCES DataArchive(UpdateID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `DataDeletion` (
  `DeletionID` integer PRIMARY KEY AUTO_INCREMENT,
  `UpdateID` integer NOT NULL,
  `DeletionDate` date,
  `DataRemoved` integer,
    FOREIGN KEY (UpdateID) REFERENCES DataArchive(UpdateID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS `StudentPermissions` (
  `AdminInCharge` integer NOT NULL,
  `StudentID` integer NOT NULL,
  `AccessLevel` integer,
  `AccessDescription` text,
        FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS `EmployerPermissions` (
  `AdminInCharge` integer NOT NULL,
  `EmployerID` integer NOT NULL,
  `AccessLevel` integer,
  `AccessDescription` text,
    FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE,
    FOREIGN KEY (EmployerID) REFERENCES HiringManager(EmployerID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `AdminPermissions` (
  `AdminInCharge` integer NOT NULL,
  `AdminID` integer NOT NULL,
  `AccessLevel` integer,
  `AccessDescription` text,
    FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE,
    FOREIGN KEY (AdminID) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `AlertSystem` (
 `AlertID` integer PRIMARY KEY AUTO_INCREMENT,
  `AdminInCharge` integer NOT NULL,
  `ActivityType` varchar(100),
  `GeneratedBy` integer NOT NULL,
  `Description` text,
  `Severity` varchar(100),
  `Timestamp` datetime,
  `Status` varchar(100),
    FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES Student(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES HiringManager(EmployerID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `JobListingManagement` (
    `AdminInCharge` integer NOT NULL,
    `JobID` integer NOT NULL,
    `UpdateID` integer,
    FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE ,
    FOREIGN KEY (JobID) REFERENCES JobListings(JobListingID) ON DELETE CASCADE,
    FOREIGN KEY (UpdateID) REFERENCES SystemUpdate(UpdateID) ON DELETE CASCADE
);

-- Insert into Student table
INSERT INTO Student (StudentID, FirstName, LastName, Major, isMentor, WCFI)
VALUES
(1, 'Peter', 'Parker', 'Arachnology', FALSE, '1234'),
(2, 'Mary', 'Jane', 'Computer Science', TRUE, '5678');

INSERT INTO Availabilities (StudentID, StartDate, EndDate)
VALUES
(2, '2024-12-10 10:00:00', '2024-12-10 12:00:00'),
(2, '2024-12-15 08:00:00', '2024-12-15 10:00:00');

-- Insert into Resume table
INSERT INTO Resume (StudentID, ResumeName, WorkExperience, TechnicalSkills, SoftSkills)
VALUES
(1, 'Alice Resume', 'Software Developer Intern at TechCorp', 'Java, SQL', 'Communication, Leadership'),
(2, 'Bob Resume', 'Junior Engineer at BuildCo', 'CAD Design, Prototyping', 'Problem-solving, Teamwork');

--HIRING MANAGER NEW INSERT STATEMENTS ---------------------------------------
-- Insert into HiringManager table (One hiring manager for simplicity)
INSERT INTO HiringManager (ApplicantID, FirstName, LastName, Position)
VALUES
(1, 'Alex', 'Smith', 'Hiring Manager'); -- Alex is the hiring manager responsible for job postings and applicant tracking

-- Insert into Company table (A company associated with the hiring manager)
INSERT INTO Company (EmployerID, Name, Industry)
VALUES
(1, 'InnovativeTech', 'Technology');  -- InnovativeTech is the company where the hiring manager works

-- Insert into JobListings table (Hiring manager posting job openings)
INSERT INTO JobListings (JobListingID, JobDescription, JobPositionTitle, JobIsActive, CompanyID)
VALUES
(1, 'Looking for a skilled software engineer to join our team and work on innovative projects.', 'Software Engineer', TRUE, 1), -- Software Engineer position
(2, 'Seeking a data analyst to help with data-driven decision making and business intelligence projects.', 'Data Analyst', TRUE, 1); -- Data Analyst position

-- Insert into Application table (Applicants applying for job listings)
-- Assuming students have IDs 1 and 2 from previous data
INSERT INTO Application (ApplicationID, StudentID, AppliedDate, Status, JobID)
VALUES
(1, 1, '2024-12-01', 'Pending', 1),  -- Applicant 1 for Software Engineer
(2, 2, '2024-12-02', 'Interview Scheduled', 2); -- Applicant 2 for Data Analyst

-- Insert into Rank table (Automated ranking based on applicant match with job descriptions)
-- Rank is calculated based on applicant match with job description (e.g., keyword matching, skills match)
INSERT INTO Rank (ApplicantID, RankNum)
VALUES
(1, 1),  -- Applicant 1 (Software Engineer) ranked 1 (high match)
(2, 2);   -- Applicant 2 (Data Analyst) ranked 2 (moderate match)

-- Insert into Resume table (Applicants' resumes)
INSERT INTO Resume (StudentID, ResumeName, WorkExperience, TechnicalSkills, SoftSkills)
VALUES
(1, 'John Doe Resume', 'Software Developer Intern at TechCorp', 'Java, C++, SQL, Python', 'Problem-solving, Communication, Teamwork'),
(2, 'Jane Smith Resume', 'Data Analyst Intern at DataCorp', 'Excel, PowerBI, SQL', 'Critical Thinking, Communication, Attention to Detail');

-- Insert into CareerProjections table (Career projections for each applicant based on their future plans)
INSERT INTO CareerProjections (StudentID, EducationTimeline, CoopTimeline, FullTimeTimeline)
VALUES
(1, '2024-2026: B.S. in Computer Science', 'Summer 2025: TechCorp Intern', '2026: Full-time at InnovativeTech'),
(2, '2024-2026: B.S. in Data Science', 'Summer 2025: DataCorp Coop', '2026: Full-time at InnovativeTech');

-- Insert into Coop table (Co-op experiences that help the hiring manager assess applicants)
INSERT INTO Coop (StudentID, StartDate, EndDate, JobTitle, CompanyName, CoopReview, CoopRating)
VALUES
(1, '2025-06-01', '2025-08-31', 'Software Intern', 'TechCorp', 'Great technical learning experience', 5),
(2, '2025-06-01', '2025-08-31', 'Data Analyst Intern', 'DataCorp', 'Strong data analysis skills', 4);

-- Insert into MBTI_Assessments table (Work-based MBTI assessments incorporated into each applicant's profile)
-- Assuming MBTI assessment values are stored in a new table for this purpose
CREATE TABLE IF NOT EXISTS MBTI_Assessments (
  `AssessmentID` integer PRIMARY KEY AUTO_INCREMENT,
  `StudentID` integer NOT NULL,
  `MBTI_Type` varchar(4),
  `AssessmentDate` date,
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE
);

-- Insert mock MBTI assessment data for applicants
INSERT INTO MBTI_Assessments (StudentID, MBTI_Type, AssessmentDate)
VALUES
(1, 'INTJ', '2024-11-30'), -- Applicant 1: INTJ personality (Strategic and analytical)
(2, 'ENTP', '2024-12-01'); -- Applicant 2: ENTP personality (Innovative and communicative)

-- Insert into JobListingManagement table (Job status updates - Expired or Filled job listings)
-- Here we mark the Software Engineer job as filled and the Data Analyst job as expired
INSERT INTO JobListingManagement (AdminInCharge, JobID, UpdateID)
VALUES
(1, 1, 1), -- Job listing for Software Engineer filled by hiring manager Alex Smith
(1, 2, 2); -- Job listing for Data Analyst expired (no longer accepting applications)

-- Insert into SystemUpdate table (System updates related to job listings)
INSERT INTO SystemUpdate (UpdateType, AdminID, UpdateDate, Description)
VALUES
('Job Listing Filled', 1, '2024-12-05', 'Software Engineer position filled by a candidate'),
('Job Listing Expired', 1, '2024-12-05', 'Data Analyst position expired, no more applicants');

---NEW HIRING MANAGER INSERTS END----------------------------------------------------------------------------------------------------------------------
-- Insert into HiringManager table
INSERT INTO HiringManager (ApplicantID,FirstName, LastName, Position)
VALUES
(1, 'John', 'Doe', 'Technical Lead'),
(2, 'Jane', 'Roe', 'Engineering Manager');

-- Insert into Company table
INSERT INTO Company (EmployerID, Name, Industry)
VALUES
(1, 'TechCorp', 'Technology'),
(2, 'BuildCo', 'Engineering');

INSERT INTO JobListings (JobListingID, JobDescription, JobPositionTitle, JobIsActive, CompanyID)
VALUES
(3, 'Software Engineer Intern', 'Software Intern', TRUE, 1),
(4, 'Mechanical Engineer Intern', 'Mechanical Intern', TRUE, 2);

-- Insert into CareerProjections table
INSERT INTO CareerProjections (StudentID, EducationTimeline, CoopTimeline, FullTimeTimeline)
VALUES
(1, '2024-2026: B.S. Computer Science', 'Summer 2025: TechCorp Intern', '2026: Full-time at TechCorp'),
(2, '2024-2026: B.S. Mechanical Engineering', 'Summer 2025: BuildCo Coop', '2026: Full-time at BuildCo');

-- Insert into Coop table
INSERT INTO Coop (StudentID, StartDate, EndDate, JobTitle, CompanyName, CoopReview, CoopRating)
VALUES
(1, '2025-06-01', '2025-08-31', 'Software Intern', 'TechCorp', 'Great learning experience', 5),
(2, '2025-06-01', '2025-08-31', 'Mechanical Engineering Coop', 'BuildCo', 'Great team collaboration', 4);

-- Insert into Availabilities table
INSERT INTO Availabilities (StudentID, StartDate, EndDate)
VALUES
(1, '2024-12-01 09:00:00', '2024-12-01 17:00:00'),
(2, '2024-12-02 09:00:00', '2024-12-02 17:00:00');

-- Insert into Appointment table
INSERT INTO Appointment (MentorID, MenteeID, AvailabilityID, AppointmentDate, Duration, MeetingSubject)
VALUES
(1, 2, 1, '2024-12-01 10:00:00', 60, 'Career Advice'),
(2, 1, 2, '2024-12-02 14:00:00', 45, 'Engineering Insights');

-- Insert into Rank table
INSERT INTO `Rank` (ApplicantID, RankNum)
VALUES
(1, 2),
(2, 1);

-- Insert into SystemsAdministrator table
INSERT INTO SystemsAdministrator (FirstName, LastName)
VALUES
('John', 'Doe'),
('Jane', 'Smith');

-- Insert into SystemUpdate table
INSERT INTO SystemUpdate (UpdateType, AdminID, UpdateDate, Description)
VALUES
('Security Patch', 1, '2024-11-01', 'Applied a security patch for vulnerabilities'),
('System Maintenance', 2, '2024-11-05', 'Scheduled system maintenance for optimization');

-- Insert into DataArchive table
INSERT INTO DataArchive (DataType, ArchiveDate, AdminID)
VALUES
('Resume Data', '2024-11-01', 1),
('Job Listings', '2024-11-05', 2);

-- Insert into DataBackup table
INSERT INTO DataBackup (UpdateID, BackupDate, DataSize)
VALUES
(1, '2024-11-02', 500),
(2, '2024-11-06', 300);

-- Insert into DataDeletion table
INSERT INTO DataDeletion (UpdateID, DeletionDate, DataRemoved)
VALUES
(1, '2024-11-03', 200),
(2, '2024-11-07', 150);


-- Insert into StudentPermissions table
INSERT INTO StudentPermissions (AdminInCharge, StudentID, AccessLevel, AccessDescription)
VALUES
(1, 1, 1, 'Full Access to Dashboard'),
(2, 2, 2, 'Limited Access to Job Listings');

-- Insert into EmployerPermissions table
INSERT INTO EmployerPermissions (AdminInCharge, EmployerID, AccessLevel, AccessDescription)
VALUES
(1, 1, 1, 'Full Access to Job Listings'),
(2, 2, 2, 'Limited Access to Applicant Data');

-- Insert into AdminPermissions table
INSERT INTO AdminPermissions (AdminInCharge, AdminID, AccessLevel, AccessDescription)
VALUES
(1, 1, 1, 'Super Admin Permissions'),
(2, 2, 2, 'Data Manager Permissions');

SELECT * FROM Availabilities WHERE StudentID = 2;
-- Insert expired job listings into the JobListings table
INSERT INTO JobListings (JobListingID, JobDescription, JobPositionTitle, JobIsActive, CompanyID)
VALUES
(5, 'Expired Job 1 Description', 'Expired Position 1', FALSE, 1),
(6, 'Expired Job 2 Description', 'Expired Position 2', FALSE, 2),
(7, 'Expired Job 3 Description', 'Expired Position 3', FALSE, 1);

