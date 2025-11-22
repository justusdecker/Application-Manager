# Automatic-Documentator by Justus Decker

# .//main.py

## err_return
Returns a simple template for debugging purposes.

## delete_job
Deletes the entry of a job in the Database.
Redirects to show_jobs

## read_job
Shows the information about a Job

## update_job
For updating an existing Job in the Database

GET:
    Let the user create a new job
POST:
    Adds the Job to the Database
    Redirects to show_jobs
! Has no ID verification

## create_job
For creating a new Job in the Database

GET:
    Let the user create a new job
POST:
    Adds the Job to the Database
    Redirects to jobs/read/-1
! Has no ID verification

## show_jobs
Shows all jobs, listed in the database.
* Fix the id problem(ID -> Text Translation)

## index
Index redirects to /Jobs

# ./src/data.py

# ./src/errors.py

# ./src/mail.py

# ./src/version.py

