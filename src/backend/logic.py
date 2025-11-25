from src.backend.flask_main import *
from src.data import JOBS, JOBIDS, JobApplianceStates
from typing import Callable

@app.route('/jobs/delete/<id>',methods = [POST])
def delete_job(id: int):
    """
    Deletes the entry of a job in the Database.
    Redirects to show_jobs with id = -1
    """
    JOBS.delete(id)
    return redirect(url_for('show_jobs'))

@app.route('/jobs/read/<id>',methods = [GET])
def read_job(id: int):
    """
    Shows the information about a Job
    redirect to itself with data id if data id is not input
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
    redirect to itself with data id if data id is not input
    GET:
        Let the user create a new job
    POST:
        Adds the Job to the Database
        Redirects to show_jobs with id = -1
    """
    if request.method.upper() == POST:
        JOBS.update(id = id, **request.form)
        return redirect(url_for('show_jobs'))
    
    jobs = JOBIDS.read_all(True)
    data = JOBS.read_as_dict(id, JOBIDS)
    
    if data is None: return "Error occured"
    
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
    """
    template = render_template(
        'jobs_c.html',
        jobs = JOBIDS.read_all(True),
        states = JobApplianceStates.get()
        ), 200
    
    if request.method.upper() == POST:
        JOBS.create(**request.form)

        return template
    
    return template

@app.route('/jobs',methods = [GET])
def show_jobs():
    """
    Shows all jobs, listed in the database.
    """
    return render_template('jobs_s.html',
                           jobs=JOBS.read_all(True, JOBIDS))
    
@app.route('/job_titles/create',methods = [POST, GET])
def create_job_title():
    if request.method.upper() == POST:
        name = request.form.get('name')

        JOBIDS.create(name = name)

        return redirect(url_for('read_job_title',id="-1"))
    
    return render_template(
        'job_title_c.html',
        jobs = JOBIDS.read_all(),
        states = JobApplianceStates.get()
        ), 200
    
@app.route('/job_titles/read/<id>',methods = [GET])
def read_job_title(id: int):
    
    data = JOBIDS.read_as_dict(id)
    
    if str(data['id']) != str(id):
        return redirect(url_for('read_job_title',id=data['id']))
    
    return render_template(
        'job_title_r.html',
        values = data
    )
    
@app.route('/job_titles/update/<id>',methods = [POST, GET])
def update_job_title(id: int):
    data = JOBIDS.read_as_dict(id)
    
    if str(data['id']) != str(id):
        return redirect(url_for('read_job_title',id=data['id']))
    
    if request.method.upper() == POST:
        JOBIDS.update(id = id, **request.form)
        return redirect(url_for('show_job_titles'))
    
    
    return render_template(
        'job_title_u.html',
        job_ids = data
        ), 200

@app.route('/job_titles/delete/<id>',methods = [POST])
def delete_job_title(id: int):
    JOBIDS.delete(id)
    return redirect(url_for('show_job_titles'))

@app.route('/job_titles',methods = [GET])
def show_job_titles():
    return render_template(
        'job_title_s.html',
        jobs = JOBIDS.read_all(True),
        states = JobApplianceStates.get()
        ), 200
    
