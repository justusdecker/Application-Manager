# Automatic-Documentator by Justus Decker

# .//ai_api.py

## improve_writing
Returns a improved version of the text you input.

Uses the Masterschool API.

# .//main.py

## err_return
Returns a simple template for debugging purposes.

## index
Index redirects to /Jobs

# ./src/data.py

## SQL
A generic wrapper for CRUD operations (Create, Read, Update, Delete)
on a specific SQLAlchemy model.

## JobIds
Specialized Class for JobId-Operations.
Inherits all CRUD-Functions from SQL & expand it by JobId-specific logic.

## Jobs
Specialized Class for Job-Operations.
Inherits all CRUD-Functions from SQL and expand these by Job-Logic.

## read
Retrieves a record by its ID.

Behavior:
    Uses `validate_id_and_get`. If the provided ID is invalid or 
    cannot be found, this method falls back to returning the 
    last (newest) entry in the table.

Args:
    id (int | str): The ID to search for.

Returns:
    Object | None: The found database object or the last entry as fallback.
                   Returns None if the table is empty.

## create
Creates a new record.

Args:
    **data: Keyword arguments matching the column names of the table.

Returns:
    bool: True if successful, None if an error occurred (e.g., IntegrityError).

## delete
Deletes a record by its ID.

Safety:
    Unlike `read`, this method performs NO fallback. If the ID does 
    not exist exactly, nothing happens. This prevents accidental 
    deletion of wrong data.

Args:
    id (int | str): The ID of the record to delete.

Returns:
    bool: True if commit was successful, None on database error.
    None: If the ID was not found.

## update
Updates an existing record.

Safety:
    Like `delete`, this method performs NO fallback. Only exact ID matches
    will be updated.

Args:
    id (int | str): The ID of the record to update.
    **data: The fields to update (key=value). Keys that do not exist 
            in the model are ignored.

Returns:
    bool: True if commit was successful (or nothing changed).
    None: If the ID was not found.

## commit
Executes the database commit and handles errors.

Returns:
    bool: True on success, None on error (triggers rollback).

## validate_id_and_get
Attempts to safely retrieve an object (with fallback logic).

Logic:
1. Tries to convert the ID to an integer.
2. Tries to load the object directly via Primary Key (Fast).
3. If 1 or 2 fails: Loads the last (newest) entry of the table as a fallback.

Args:
    id (str | int): The raw ID.

Returns:
    Object | None: The found object or None if table is empty/error.

## create
Creates a new job with the given name

## update
Updates the name of a job.

## read_all
Reads all jobs.

if as_dict: gives you a list[dict]
else: gives you a list[SQLTable]

## read_as_dict
Reads a single jb & returns it as dictionary

## get_job_name
Gets only the job name corresponding to the id

## get_ids
Gets the list of existing ids

## get_last_entry
Gets the last(newest) JobId-Object.

## _to_dict
Internal Helper: Converts SQLAlchemy Object to dict.

## create
Creates a new job-entry.
### Valid data:

    company: str, 
    title_id: int, 
    url: str, 
    mail: str, 
    phone_number: str, 
    description: str, 
    state_id: int

## update
Updates the Job-Entry

### Valid data:

    company: str, 
    title_id: int, 
    url: str, 
    mail: str, 
    phone_number: str, 
    description: str, 
    state_id: int

## read_as_dict
Reads a single job-entry and returns it as dict.
Returns None if id does not exist

## get_last_id
Returns the last id in the table or None

## _to_dict
Internal Helper: Converts SQLAlchemy Object to dict

# ./src/errors.py

# ./src/gemini_api.py

# ./src/linkedin_job_search_fetch.py

## fetch_linkedin_job_data
Gets you the logo, job_title, company_name, description & also returns the job_id in the dict.

## fetch_job_ids
Takes a html-structure in string form, runs the HTML parser and fetches the job ids from there.
For this to work you need to copy the html from your browser and paste this into a file!

# ./src/mail.py

# ./src/validation.py

# ./src/version.py

# ./src/backend/flask_main.py

# ./src/backend/logic.py

## delete_job
Deletes the entry of a job in the Database.
Redirects to show_jobs with id = -1

## read_job
Shows the information about a Job
redirect to itself with data id if data id is not input

## update_job
For updating an existing Job in the Database
redirect to itself with data id if data id is not input
GET:
    Let the user create a new job
POST:
    Adds the Job to the Database
    Redirects to show_jobs with id = -1

## create_job
For creating a new Job in the Database

GET:
    Let the user create a new job
POST:
    Adds the Job to the Database
    Redirects to jobs/read/-1

## show_jobs
Shows all jobs, listed in the database.

# ./src/backend/techstack.py

