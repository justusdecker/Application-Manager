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

# .//t.py

# ./src/constants.py

# ./src/flask_main.py

# ./src/version.py

# ./src/backend/data.py

Contains all file-accesses, Table-definitions, SQL-interactions & other file-related functions, classes for the runtime.

## sfa
single-file-access
you dont need to write the 'with' stuff anymore :D

Does the same as context manager open()
```python
with open(fp, m) as f:
    return f.read()
    return f.read() -> str | return f.write(d) -> None
```

Args:
    fp (str): filepath
    m (str): mode
    d (str, optional): data. Defaults to None.

Raises:
    TypeError: If the mode is writing and the data is None

Returns:
    str | None: The read-data if mode `r`

## create_file_if_not_exist
Will create a file with the `default_data` if file does not exist.

Args:
    filepath (str)
    default_data (str): If the file does not exist, this data will be written to the `filepath`

## file_read
Reads from `filepath` in mode: `r`

Args:
    filepath (str)

Returns:
    str: the data that the file contains

## file_write
Writes `data` to `filepath` in mode: `w`

Args:
    filepath (str)
    data (str)

## JobApplianceStates
A simple Dataclass used for the State in the job-appliance.

Used for the read, show page for jobs.

```python
INVALID = -1
NOT_APPLIED = 0
APPLIED = 1
SCREEN = 2
INTERVIEW = 3
OFFER = 4
DENIED = 5
```

## JobIdsTable
The JobIdsTable alias(Job-title or Profession)

## JobsTable
The Jobs-Table

## LinkedInJobsTable
The LinkedInJobsTable

This is a "temp" Database so the Jobs-DB(The jobs you apply to) is not crowded everytime the user imports from linkedIn.

## CVCTable
The CVCTable

> [!ATTENTION]
> Only store the python-script in the `cvc` column.
> Otherwise the app will not work!

## SQL
A generic wrapper for CRUD operations (Create, Read, Update, Delete)
on a specific SQLAlchemy model.

## JobIds
Specialized Class for JobId-Operations.
Inherits all CRUD-Functions from SQL & expand it by JobId-specific logic.

## Jobs
Specialized Class for Job-Operations.
Inherits all CRUD-Functions from SQL and expand these by Job-Logic.

## LinkedInJobs
Specialized Class for LinkedInJob-Operations.
Inherits all CRUD-Functions from SQL and expand these by LinkedInJob-Logic.

## CVC
Specialized Class for CV-Operations.
Inherits all CRUD-Functions from SQL and expand these by CV-Logic.

## connect
Creates the SQL Engine & Session for the runtime

## get
gives you all states

Returns:
    list[tuple[str, int]]: [`name`, `id`]

## _get_state_as_text
Args:
    id (int): the id you want to get the name of

Returns:
    str: the name

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

## get_job_exist
Args:
    name (str): the name of the job

Returns:
    int | False: The corresponding id or False

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

## read_all
Reads all job-entrys

## read_as_dict
Reads a single job-entry and returns it as dict.
Returns None if id does not exist

## get_last_id
Returns the last id in the table or None

## _to_dict
Internal Helper: Converts SQLAlchemy Object to dict

## create
Creates a new linkedInjob-entry.
### Valid data:

    company: str, 
    job_title: int,
    lid: int, 
    description: str,
    logo: str

## update
Updates the LinkedInJob-Entry

### Valid data:

    company: str, 
    job_title: int,
    lid: int, 
    description: str,
    logo: str

## read_all
Reads all LinkedInjob-entrys

## read_as_dict
Reads a single LinkedInjob-entry and returns it as dict.
Returns None if id does not exist

## is_lid_inthere
Args:
    lid (str): the linkedIn id

Returns:
    bool: Is linkedIn id in the database?

## get_last_id
Returns the last id in the table or None

## _to_dict
Internal Helper: Converts SQLAlchemy Object to dict

## create
Creates a new CV-entry.
### Valid data:

    cvc: str
    name: str

## update
Updates the CV-Entry

### Valid data:
    cvc: str
    name: str

## read_all
Reads all CV-entrys

## read_as_dict
Reads a single CV-entry and returns it as dict.
Returns None if id does not exist

## get_last_id
Returns the last id in the table or None

## _to_dict
Internal Helper: Converts SQLAlchemy Object to dict

# ./src/backend/gemini_api.py

The Gemini API Access

To use this you must create a .env file in the root directory with the `GOOGLE_API_KEY` inside.

## configuration
Load the `GOOGLE_API_KEY` from the .env File

## create_payload
Create & get the JSON structure required for the Gemini API

## send_gemini
Sends a POST Request to gemini & receives the generated `text` from it.

Returns the gemini result -> `str`.

If a error occoures: 
    returns a dict that only contains the `error`.

# ./src/backend/linkedin_job_search_fetch.py

## fetch_linkedin_job_data
Gets you the logo, job_title, company_name, description & also returns the job_id in the dict.

## fetch_job_ids
Takes a html-structure in string form, runs the HTML parser and fetches the job ids from there.
For this to work you need to copy the html from your browser and paste this into a file!

# ./src/backend/logic.py

## delete_job
Deletes the entry of a job in the Database.
Redirects to show_jobs with id = -1

## read_job
Shows the information about a single Job
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

## create_job_title
For creating a new Job-title in the Database

GET:
    Let the user create a new job-title
POST:
    Adds the Job-title to the Database
    Redirects to job_titles/read/-1

## export_json
Downloads the jobs-database as json.

## export_csv
Downloads the jobs-database as csv.

## create_job_from_linkedin
company: str, 
title_id: int, 
url: str, 
mail: str, 
phone_number: str, 
description: str, 
state_id: int

edge cases:
    - job-title does not exist
    

# ./src/backend/mail.py

# ./src/backend/search.py

## LowerCaseStr
The string should be in lower-case
For performance & case-insensitive search reasons.
    
```python
a: str = "".lower()
```

# ./src/backend/validation.py

# ./src/backend/cv_creator/cv_generator.py

# ./src/backend/cv_creator/objects.py

## Links
Represents a collection of hyperlinked text elements, typically for a sidebar,
and generates the corresponding HTML string.

## Head
Represents a main heading for a section, typically in a sidebar,
and generates the corresponding HTML string.

## Title
Represents a sub-title or secondary heading, typically in a sidebar,
and generates the corresponding HTML string.

## Content
Represents a block of general text content, typically in a sidebar,
and generates the corresponding HTML string.

## Bulletpoint
Represents a single bullet point item, and generates the corresponding HTML string.
Note: This does not wrap the content in a standard HTML list (ul/li).

## Project
A data structure class representing a project entry, likely for a resume or portfolio.
It holds data but does not generate HTML itself.

## EducationOrExperience
A data structure class representing an entry for education or professional experience.
It holds data but does not generate HTML itself.

## get
Generates the HTML string containing all links, enclosed in a div with
specific sidebar styling.

:return: An HTML string of linked titles separated by ", ".

## get
Generates the HTML string for the heading, wrapped in a div with
border and main title styling.

:return: An HTML string for the section heading.

## get
Generates the HTML string for the sub-title, wrapped in a div with
secondary title styling.

:return: An HTML string for the sub-title.

## get
Generates the HTML string for the content, wrapped in a div and a paragraph
tag with specific sidebar text styling.

:return: An HTML string for the content block.

## get
Generates the HTML string for the bullet point content, wrapped in a paragraph
tag with a specific class for viewing.

:return: An HTML string for the bullet point.

