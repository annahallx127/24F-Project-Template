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
    FOREIGN KEY (UpdateID) REFERENCES SystemUpdate(UpdateID) ON DELETE CASCADE
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

-- Insert into Availabilities table
INSERT INTO Availabilities (AvailabilityID, StudentID, StartDate, EndDate)
VALUES
(1, 2, '2024-12-10 10:00:00', '2024-12-10 12:00:00'),
(2, 2, '2024-12-15 08:00:00', '2024-12-15 10:00:00');

-- Insert into Resume table
INSERT INTO Resume (ResumeID, StudentID, ResumeName, WorkExperience, TechnicalSkills, SoftSkills)
VALUES
(1, 1, 'Peter Resume', 'Entomology Intern at Central Park Zoo', 'PCR, Sanger sequencing, BLAST', 'Communication, Leadership'),
(2, 2, 'Mary Resume', 'Software Developer Intern at Google', 'Java, C++', 'Problem-solving, Teamwork, Leadership');

-- Hiring Manager Insert Statement--------------------------
INSERT INTO HiringManager (EmployerId,ApplicantID, FirstName, LastName, Position)
VALUES
(1, 2, 'Miles', 'Moralas','Hiring Manager');


INSERT INTO Company (CompanyID, EmployerID, Name, Industry)
VALUES
(1, 1, 'SpiderVerse','Arachnology Software');

INSERT INTO JobListings (JobListingID,CompanyID,JobDescription, JobPositionTitle, JobIsActive)
VALUES
(1, 1, 'Looking for a software engineer with REQUIRED experience in Python, Java, SQL, C++, and modern frameworks like Django and Flask. Must have strong problem-solving skills. $90,000 annually with benefits.', 'Software Engineer', TRUE),
(2, 1, 'Seeking a Researcher with a strong background in arachnology to assist with field studies and species classification. Must have prior lab and fieldwork experience.', 'Arachnology Researcher', TRUE),
(3, 1, 'Looking for a Full Stack Developer proficient in React.js, Node.js, and TypeScript. This role is remote-friendly and offers competitive compensation.', 'Full Stack Developer', TRUE),
(4, 1, 'Hiring a Data Scientist with expertise in machine learning, Python, and R. Must be capable of building predictive models and analyzing large datasets.', 'Data Scientist', TRUE),
(5, 1, 'Seeking an Arachnology Technician for on-site research focused on venom composition analysis. Must be comfortable handling live specimens.', 'Arachnology Technician', TRUE),
(6, 1, 'Hiring a Mobile App Developer with experience in Kotlin and Swift to develop cross-platform applications for research and education.', 'Mobile App Developer', TRUE),
(7, 1, 'Looking for an AI/ML Engineer with experience in deep learning frameworks (TensorFlow, PyTorch) and natural language processing.', 'AI/ML Engineer', TRUE),
(8, 1, 'Opening for a Database Administrator with expertise in SQL, MongoDB, and cloud services like AWS RDS. Will manage large-scale data for computational biology.', 'Database Administrator', TRUE),
(9, 1, 'Seeking an Arachnology Field Researcher to conduct field surveys on spider populations and document ecological data. Must have prior experience with taxonomy and habitat analysis.', 'Arachnology Field Researcher', TRUE),
(10, 1, 'Hiring an Arachnology Laboratory Assistant to assist in studying arachnid venom and silk properties. Must be skilled in microscopy and chemical analysis.', 'Arachnology Laboratory Assistant', TRUE),
(11, 1, 'Looking for a Wildlife Photographer specializing in arachnids to document rare species for a research database. Prior experience in macro photography is required.', 'Arachnid Wildlife Photographer', TRUE),
(12, 1, 'Opening for an Arachnology Educator to create engaging content about arachnids for museums and educational platforms. Experience in public outreach is a plus.', 'Arachnology Educator', TRUE),
(13, 1, 'Seeking a Spider Silk Engineer to study and replicate silk properties for use in biotechnological applications. Background in biomaterials is essential.', 'Spider Silk Engineer', TRUE),
(14, 1, 'Hiring a Biodiversity Analyst specializing in arachnids to analyze datasets and create conservation strategies for endangered spider species.', 'Arachnid Biodiversity Analyst', TRUE),
(15, 1, 'Looking for an Arachnid Behavioral Ecologist to study spider hunting and mating behaviors in controlled environments. Must have expertise in experimental design.', 'Arachnid Behavioral Ecologist', TRUE),
(16, 1, 'Seeking an Arachnid Conservation Specialist to develop programs aimed at protecting endangered spider and scorpion species in urban and rural areas.', 'Arachnid Conservation Specialist', TRUE),
(17, 1, 'Hiring an Entomologist with a focus on arachnids to contribute to a cross-species study on pest control and ecological impacts. Must have a PhD or equivalent experience.', 'Entomologist (Arachnid Focus)', TRUE),
(18, 1, 'Looking for a Venom Chemist to analyze the chemical composition of spider and scorpion venom for pharmaceutical applications. Experience in toxicology required.', 'Venom Chemist', TRUE),
(19, 1, 'Seeking an Arachnology Data Curator to manage and digitize records of spider species in collaboration with global biodiversity databases.', 'Arachnology Data Curator', TRUE),
(20, 1, 'Hiring a Research Assistant to assist in a study on the impact of climate change on arachnid populations. Fieldwork and GIS experience are required.', 'Arachnology Research Assistant', TRUE);


-- Insert into Application table
INSERT INTO Application (ApplicationID, StudentID, AppliedDate, Status, JobID)
VALUES
(1, 1, '2024-12-06', 'Pending', 2),  -- Arachnology Researcher
(2, 1, '2024-12-03', 'Pending', 5),  -- Arachnology Technician
(3, 1, '2024-11-30', 'Accepted', 9),  -- Arachnology Field Researcher
(4, 1, '2024-12-01', 'Applied', 10),  -- Arachnology Laboratory Assistant
(5, 1, '2024-12-04', 'Pending', 13),  -- Spider Silk Engineer
(6, 1, '2024-12-02', 'Rejected', 18),  -- Venom Chemist
(7, 2, '2024-12-06', 'Pending', 1),  -- Software Engineer
(8, 2, '2024-11-28', 'Interview', 3),  -- Full Stack Developer
(9, 2, '2024-12-03', 'Pending', 4),  -- Data Scientist
(10, 2, '2024-12-05', 'Rejected', 6);  -- Mobile App Developer


INSERT INTO CareerProjections (TimelineID,StudentID,EducationTimeline,CoopTimeline,FullTimeTimeline)
VALUES
(1,2,'Plus one program - adding one year to your time at northeastern but graduating with a masters degree','Previous experience in SWE, Data Anlayst, roles','Reccomended full time in SWE role');

INSERT INTO Coop(CoopID, StudentID, StartDate, EndDate, JobTitle, CompanyName, CoopReview, CoopRating)
VALUES
(1,1,'2024-12-04','2025-06-18','SWE at Apple','Apple Inc.','Very nice co-op I got a lot of free merch', 5);

INSERT INTO `Rank` (ApplicantID, RankNum)
VALUES
(1,2),
(2,1);

INSERT INTO Appointment(AppointmentID, MentorID, MenteeID, AvailabilityID, AppointmentDate, Duration, MeetingSubject)
VALUES
(1, 2, 1, 1, '2024-12-10 10:00:00', 2, 'Discuss Jobs')


-- System Administrator Insert Statements --
INSERT INTO SystemsAdministrator (AdminID, FirstName, LastName)
VALUES
(1, 'Gwen', 'Stacy'),
(2, 'Mary', 'Jane');

INSERT INTO SystemUpdate (UpdateID, UpdateType, AdminID, UpdateDate)
VALUES
(1, 'Delete Old Data', 1, '2024-10-13'),
(2, 'System Update Version 12', 2, '2024-08-25');

INSERT INTO DataArchive (UpdateID, DataType, ArchiveDate, AdminID)
VALUES
(1, 'Old Users', '2024-04-26', 2),
(2, 'EmployerIDs', '2024-09-09', 1);

INSERT INTO DataBackup (BackupID, UpdateID, BackupDate, DataSize)
VALUES
(1, 1, '2023-04-06', 6400),
(2, 2, '2024-09-04', 127000);

INSERT INTO DataDeletion (DeletionID, UpdateID, DeletionDate, DataRemoved)
VALUES
(1, 1, '2024-08-15', 500),
(2, 2, '2024-02-29', 127);

INSERT INTO StudentPermissions (AdminInCharge, StudentID, AccessLevel, AccessDescription)
VALUES
(1, 1, 2, 'Can apply for Co-op'),
(2, 2, 4, 'Can apply for Co-op and submit Coffee Chat Availibility');

INSERT INTO EmployerPermissions (AdminInCharge, EmployerID, AccessLevel, AccessDescription)
VALUES
(1, 1, 5, 'Can Post new job openings');

INSERT INTO AdminPermissions (AdminInCharge, AdminID, AccessLevel, AccessDescription)
VALUES
(1, 1, 5, 'High Level Access'),
(2, 2, 5, 'High Level Access');

INSERT INTO AlertSystem (AlertID, AdminInCharge, ActivityType, GeneratedBy, Description, Severity, TimeStamp, Status)
VALUES
(1, 2, 'Glitch', 1, 'User has experienced a glitch when logging into their account', 2, '2024-12-10 10:00:00', 'Resolved'),
(2, 1, 'Lag', 1, 'User experienced a lag when changing pages', 1, '2024-10-12 12:22:22', 'Resolved');

INSERT INTO JobListingManagement (AdminInCharge, JobID, UpdateID)
VALUES
(1, 1, 1),
(2, 1, 2);

