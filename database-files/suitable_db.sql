DROP DATABASE IF EXISTS suitable;

CREATE DATABASE IF NOT EXISTS suitable;
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
    `CompanyName` varchar(200),
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

CREATE TABLE IF NOT EXISTS `Application` (
  `ApplicationID` integer PRIMARY KEY AUTO_INCREMENT,
    `JobID` integer NOT NULL UNIQUE,
  `StudentID` integer NOT NULL,
  `CompanyName` varchar(200),
    `CompanyID` integer NOT NULL,
  `AppliedDate` date,
  `Status` varchar(30),
  `JobTitle` varchar(100),
  `JobDescription` mediumtext,
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE,
      FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Applicant` (
  `ApplicantID` integer NOT NULL PRIMARY KEY,
  `FirstName` varchar(50),
  `LastName` varchar(50),
  `Resume` text,
  `WCFI` char(4),
    FOREIGN KEY (ApplicantID) REFERENCES Application(ApplicationID) ON DELETE CASCADE
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
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) ON DELETE CASCADE
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
    FOREIGN KEY (ApplicantID) REFERENCES Applicant(ApplicantID) ON DELETE CASCADE
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

CREATE TABLE IF NOT EXISTS `JobListings` (
  `JobID` integer NOT NULL,
  `isExpired` boolean,
    FOREIGN KEY (JobID) REFERENCES Application(JobID) ON DELETE CASCADE
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
  `GeneratedBy` integer,
  `Description` text,
  `Severity` varchar(100),
  `Timestamp` datetime,
  `Status` varchar(100),
    FOREIGN KEY (AdminInCharge) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES Student(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES HiringManager(EmployerID) ON DELETE CASCADE,
    FOREIGN KEY (GeneratedBy) REFERENCES SystemsAdministrator(AdminID) ON DELETE CASCADE
);


-- Insert into Student table
INSERT INTO Student (FirstName, LastName, Major, isMentor, WCFI)
VALUES
('Alice', 'Johnson', 'Computer Science', TRUE, '1234'),
('Bob', 'Smith', 'Mechanical Engineering', FALSE, '5678');

-- Insert into Resume table
INSERT INTO Resume (StudentID, ResumeName, WorkExperience, TechnicalSkills, SoftSkills)
VALUES
(1, 'Alice Resume', 'Software Developer Intern at TechCorp', 'Java, SQL', 'Communication, Leadership'),
(2, 'Bob Resume', 'Junior Engineer at BuildCo', 'CAD Design, Prototyping', 'Problem-solving, Teamwork');

-- Insert into HiringManager table
INSERT INTO HiringManager (ApplicantID, CompanyName, FirstName, LastName, Position)
VALUES
(1, 'TechCorp', 'John', 'Doe', 'Technical Lead'),
(2, 'BuildCo', 'Jane', 'Roe', 'Engineering Manager');

-- Insert into Company table
INSERT INTO Company (EmployerID, Name, Industry)
VALUES
(1, 'TechCorp', 'Technology'),
(2, 'BuildCo', 'Engineering');

-- Insert into Application table
INSERT INTO Application (StudentID, JobID, CompanyName, CompanyID, AppliedDate, Status, JobTitle, JobDescription)
VALUES
(1, 1, 'TechCorp', 1, '2024-11-01', 'Pending', 'Software Engineer', 'Develop and maintain software applications.'),
(2, 2, 'BuildCo', 2, '2024-11-02', 'Interview Scheduled', 'Mechanical Engineer', 'Design and analyze mechanical systems.');

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

INSERT INTO `Applicant` (ApplicantID, FirstName, LastName, Resume, WCFI)
VALUES
(1, 'John', 'Doe', 'Resume text for John Doe', 'W123'),
(2, 'Jane', 'Smith', 'Resume text for Jane Smith', 'W456');


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

-- Insert into JobListings table
INSERT INTO JobListings (JobID, isExpired)
VALUES
(1, FALSE),
(2, TRUE);

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

