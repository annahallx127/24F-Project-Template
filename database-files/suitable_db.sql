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
(1, 2, 5, 'Miles', 'Morales','Hiring Manager');

----Company Insert Statement---------------
INSERT INTO Company (CompanyID, EmployerID, Name, Industry)
VALUES
(21, 1, 'Miles Morales','Software');

------------JobListings Insert Statements------------
INSERT INTO JobListings (JobListingID,CompanyID,JobDescription, JobPositionTitle, JobIsActive)
VALUES
(1,21,'Looking for a software engineer with REQUIRED experience in kotlin,java,sql,html,C++,C,Racket,Assembly,javascript, R, ruby, rust, perl, babbage. Must know all languages fluently to apply. $15 an hour ', 'SWE Role (HIGH PAYING)', true);

-- Insert into Application table
INSERT INTO Application (ApplicationID, StudentID, AppliedDate, Status, JobID)
VALUES
(1, 1, '2024-12-06', 'Pending', 1),
(2, 2, '2024-12-02', 'Applied', 1);

----CareerProjections Insert Statement------------
INSERT INTO CareerProjections (TimelineID,StudentID,EducationTimeline,CoopTimeline,FullTimeTimeline)
VALUES
(1,2,'Plus one program - adding one year to your time at northeastern but graduating with a masters degree','Previous experience in SWE, Data Anlayst, roles','Reccomended full time in SWE role');

-----------------Coop Insert Statement ---------------------------------
INSERT INTO Coop(CoopID, StudentID, StartDate, EndDate, JobTitle, CompanyName, CoopReview, CoopRating)
VALUES
(1,1,2024-12-04,2025-06-18,'SWE at Apple','Apple Inc.','Very nice co-op I got a lot of free merch', 5);

---------Rank Insert Statement ----------------
INSERT INTO Rank (ApplicantID, RankNum)
VALUES 
(1,2);
(2,1);

--Appointment Insert Statement--
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
(3, 'Old Users', '2024-04-26', 2),
(4, 'EmployerIDs', '2024-09-09', 1);

INSERT INTO DataBackup (BackupID, UpdateID, BackupDate, DataSize)
VALUES 
(1, 5, '2023-04-06', 6400),
(2, 6, '2024-09-04', 127000);

INSERT INTO DataDeletion (DeletionID, UpdateID, DeletionDate, DataRemoved)
VALUES 
(1, 7, '2024-08-15', 500),
(2, 8, '2024-02-29', 127);

INSERT INTO StudentPermissions (AdminInCharge, StudentID, AccessLevel, AccessDescription),
VALUES 
(1, 1, 2, 'Can apply for Co-op'),
(2, 2, 4, 'Can apply for Co-op and submit Coffee Chat Availibility');

INSERT INTO EmployerPermissions (AdminInCharge, EmployerID, AccessLevel, AccessDescription),
VALUES
(1, 1, 5, 'Can Post new job openings'),
(2, 2, 5, 'Can Post new job openings');

INSERT INTO AdminPermisssions (AdminInCharge, AdminID, AccessLevel, AccessDescription)
VALUES
(1, 3, 5, 'High Level Access'),
(2, 4, 5, 'High Level Access');

INSERT INTO AlertSystem (AlertID, AdminInCharge, ActivityType, GeneratedBy, Description, Severtiy, TimeStamp, Status)
VALUES
(1, 2, 'Glitch', 4, 'User has experienced a glitch when logging into their account', 2, '2024-12-10 10:00:00', 'Resolved')
(2, 1, 'Lag', 4, 'User experienced a lag when changing pages', 1, '2024-10-12 12:22:22', 'Resolved')

INSERT INTO JobListingManagement (AdminInCharge, JobID, UpdateID)
VALUES
(1, 1, 1),
(2, 2, 2);

