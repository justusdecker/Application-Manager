# Automatic-Documentator by Justus Decker

# .//main.py

## err_return
Returns a simple template for debugging purposes.

## index
Index redirects to /Jobs

# ./src/data.py

## validate_id
Validates and sanitizes a string ID for database lookup.

This function attempts to convert the input ID string to an integer. 
If the conversion fails or results in a default invalid value (e.g., -1 
from `integer_or_default`), the ID is set to the index of the last record 
in the `table` (i.e., `count - 1`).

Args:
    id: The string ID to be validated.
    table: The table to lookup

Returns:
    The validated integer ID, which will be the ID of an existing job entry.
    
    Returns **None** if the `JobsTable` is completely empty.

# ./src/errors.py

# ./src/gemini_api.py

# ./src/mail.py

# ./src/validation.py

# ./src/version.py

# ./src/backend/flask_main.py

# ./src/backend/jobs.py

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

# ./src/backend/job_titles.py

## create_job_title
For creating a new Job-Title in the Database

GET:
    Let the user create a new job-title
POST:
    Adds the Job-Title to the Database
    Redirects to job_title/read/-1
! Has no ID verification

## update_job_title
For updating an existing Job-Title in the Database

GET:
    Let the user update the job-title
POST:
    Updates the Job-Title in the Database
    Redirects to job_titles
! Has no ID verification

# ./src/backend/techstack.py

