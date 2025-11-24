from src.backend.flask_main import *
from src.data import JOBS, JOBIDS, JobApplianceStates

@app.route('/jobs/delete/<id>',methods = [DELETE, GET])
def delete_job(id: int): #! NotImplemented
    """
    Deletes the entry of a job in the Database.
    Redirects to show_jobs
    """
    JOBS.delete(id)
    return redirect(url_for('show_jobs'))

@app.route('/jobs/read/<id>',methods = [GET])
def read_job(id: int):
    """
    Shows the information about a Job
    """
    data = JOBS.read_as_dict(id, JOBIDS)
    if data is None: return "Error occured"
    
    if str(data['id']) != str(id):
        return redirect(url_for(f'read_job',id=data['id']))
    
    return render_template('jobs_r.html',
                           values = JOBS.read_as_dict(id, JOBIDS))

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
        JOBS.update(
            id = id,
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state_id = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )

        return redirect(url_for('show_jobs'))
    jobs = JOBIDS.read_as_dict(id)
    data = JOBS.read_as_dict(id, JOBIDS)
    
    if jobs is None or data is None: return "Error occured"
    
    if str(data['id']) != str(id):
        return redirect(url_for(f'update_job',id=data['id']))
    
    return render_template(
        'jobs_u.html',
        jobs = jobs,
        data = data,
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
        JOBS.create(
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state_id = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )

        return redirect(f'read/-1')
    
    
    return render_template(
        'jobs_c.html',
        jobs = JOBIDS.read_all(),
        states = JobApplianceStates.get()
        ), 200

@app.route('/jobs',methods = [GET])
def show_jobs():
    """
    Shows all jobs, listed in the database.
    * Fix the id problem(ID -> Text Translation)
    """
    return render_template('jobs_s.html',
                           jobs=JOBS.read_all(True, JOBIDS))