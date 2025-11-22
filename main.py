from flask import Flask,jsonify, render_template, request, redirect, url_for
from src.data import JobsTable, JobIdsTable, JobID, Job, JobApplianceStates
from src.errors import  http_status_codes
app = Flask(__name__)

GET, POST, DELETE = 'GET', 'POST', 'DELETE'

def err_return(code: int = 404):
    """
    Returns a simple template for debugging purposes.
    """
    return render_template('error.html', err=code, msg=http_status_codes[code]), code

class JobQuery:
    def __init__(self, query: list[str]):
        duery = query
        self.COMPANY = duery['company']
        self.TITLE_ID = int(duery['job_title'])
        self.URL = duery['url']
        self.MAIL = duery['mail']
        self.PHONE_NUMBER = duery['phone_number']
        self.DESCRIPTION = duery['description']
        self.STATE = int(duery['state'])

@app.route('/job_titles/create',methods = [DELETE, GET])
def create_job_title():
    ...
    
@app.route('/job_titles/read',methods = [DELETE, GET])
def read_job_title():
    ...
    
@app.route('/job_title/update',methods = [DELETE, GET])
def update_job_title():
    ...

@app.route('/job_title/delete',methods = [DELETE, GET])
def delete_job_title():
    ...
    


@app.route('/tech_stack/create',methods = [DELETE, GET])
def create_tech_stack():
    ...
    
@app.route('/tech_stack/read',methods = [DELETE, GET])
def read_tech_stack():
    ...
    
@app.route('/tech_stack/update',methods = [DELETE, GET])
def update_tech_stack():
    ...

@app.route('/tech_stack/delete',methods = [DELETE, GET])
def delete_tech_stack():
    ...



@app.route('/jobs/delete/<id>',methods = [DELETE, GET])
def delete_job(id: int): #! NotImplemented
    """
    Deletes the entry of a job in the Database.
    Redirects to show_jobs
    """
    print(id)
    return redirect(url_for('show_jobs'))

@app.route('/jobs/read/<id>',methods = [GET])
def read_job(id: int):
    """
    Shows the information about a Job
    """
    print(id)
    return render_template('jobs_r.html',
                           values = Job.get_job_info(id))

@app.route('/jobs/update/<id>',methods = [GET, POST])
def update_job(id: int):
    """
    For updating an existing Job in the Database
    
    GET:
        Let the user create a new job
    POST:
        Adds the Job to the Database
        Redirects to show_jobs
    ! Has no ID verification
    """
    if request.method.upper() == POST:
        jq = JobQuery(request.form)
        
        Job.update_job(
            id = id,
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )

        return redirect(url_for('show_jobs'))
    
    
    return render_template(
        'jobs_u.html',
        jobs = JobID.get_job_ids(),
        data = Job.get_job_info_obj(id),
        states = JobApplianceStates.get()
        ), 200

@app.route('/jobs/create',methods = [GET, POST])
def create_job():
    """
    For creating a new Job in the Database
    
    GET:
        Let the user create a new job
    POST:
        Adds the Job to the Database
        Redirects to jobs/read/-1
    ! Has no ID verification
    """
    if request.method.upper() == POST:
        jq = JobQuery(request.form)
        Job.add_job(
            JobsTable(
                company = jq.COMPANY,
                description = jq.DESCRIPTION,
                mail = jq.MAIL,
                phone_number = jq.PHONE_NUMBER,
                state = jq.STATE,
                title_id = jq.TITLE_ID,
                url = jq.URL
            )
        )
        return redirect('read/-1')
    
    
    return render_template(
        'jobs_c.html',
        jobs = JobID.get_job_ids(),
        states = JobApplianceStates.get()
        ), 200

@app.route('/jobs',methods = [GET])
def show_jobs():
    """
    Shows all jobs, listed in the database.
    * Fix the id problem(ID -> Text Translation)
    """
    return render_template('jobs_s.html',
                           jobs=Job.get_all_jobs())

@app.route('/',methods = [GET])
def index():
    """
    Index redirects to /Jobs
    """
    return redirect('/jobs')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)