[Back to Main GitHub Page](https://github.com/CDarthGaming/TrackTogether/tree/main)

# Minor Patch - Version 1.1.2

* Added caption notices to the bottomn of the login & home pages

<br>

# Minor Patch - Version 1.1.1

* Fixed missing python library dependancies

<br>

# Major System Overhaul - Version 1.1

Implemented full student assignment tracking including task management, progress tracking, grading, and major system infrastructure improvements.

## Student Features
* Students can now view assignments automatically based on their course and year
* Assignment progress bars based on task completion
* Completing an assignment automatically sets progress to 100%
* Students can enter achieved grades after completing assignments
* Reminder warnings for completed assignments missing grades
* Improved assignment details view including tasks, notes, and grading
* Students no longer have the ability to create or modify assignments

## Lecturer System
* Introduced lecturer user role
* Lecturers must now be approved before gaining access
* Lecturers can assign themselves to modules they teach
* Lecturers can configure the two assignments per module
* Lecturer-created assignments automatically appear for enrolled students

## Admin & Permissions System
* Introduced admin role and permission structure
* Admins can manage users and grant admin privileges
* Admins can create and manage courses
* Admins can create modules and link them to courses and years
* Admins control lecturer approvals and overall system configuration

## Assignment & Task System
* Added per-student assignment tracking via the student_assignments table

## Database Changes
* Added student_assignments table for per-student assignment tracking
* Added progress, complete, notes, and achieved_grade fields
* Added tasks table for assignment task management
* Ensured assignments are automatically linked to students on page load
* Updated queries to correctly use student_assignments instead of assignments
* Improved SQL joins between users.db and modules.db

## Profile & Navigation Overhaul
* Completely redesigned profile menu
* Added profile picture support
* Added logout functionality
* Added ability for users to delete their account
* Overhauled the header/navigation layout

## UI Improvements
* Added assignment weighting column
* Improved layouts
* Added toast / success / warning notifications for more key user actions
* Improved assignment list readability

## Temporary Behaviour / Known Issues
* Students & lecturers temporarily have access to all module chats as the connect feature has not been fully overhauled yet
* Lecturers currently appear on the leaderboard
* Home page progress bar is currently non-functional
* These behaviours will be corrected in Version 1.2

Overall this update introduces the core academic tracking and role-based infrastructure for TrackTogether, laying the foundation for lecturer-managed assignments, student progress tracking, and admin-controlled course structures.
