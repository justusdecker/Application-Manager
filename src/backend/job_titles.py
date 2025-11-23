from src.backend.flask_main import *
from src.validation import integer_or_default
@app.route('/job_titles/create',methods = [POST, GET])
def create_job_title():
    """
    For creating a new Job-Title in the Database
    
    GET:
        Let the user create a new job-title
    POST:
        Adds the Job-Title to the Database
        Redirects to job_title/read/-1
    ! Has no ID verification
    """
    id = integer_or_default(id, -1)
    if request.method.upper() == POST:
        jq = JobQuery(request.form)
        Job.create(
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )
        return redirect(url_for('show_job_titles'))
    
    
    return render_template(
        'jobs_c.html'
        ), 200
    
@app.route('/job_titles/read',methods = [GET])
def read_job_title():
    ...
    
@app.route('/job_titles/update/<id>',methods = [POST, GET])
def update_job_title(id: int):
    """
    For updating an existing Job-Title in the Database
    
    GET:
        Let the user update the job-title
    POST:
        Updates the Job-Title in the Database
        Redirects to job_titles
    ! Has no ID verification
    """
    if request.method.upper() == POST:
        jq = JobQuery(request.form)
        Job.create(
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )
        return redirect(url_for('show_job_titles'))
    
    
    return render_template(
        'jobs_c.html'
        ), 200

@app.route('/job_titles/delete',methods = [DELETE])
def delete_job_title():
    ...