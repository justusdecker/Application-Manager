from src.backend.flask_main import *

@app.route('/jobs/delete/<id>',methods = [DELETE, GET])
def delete_job(id: int): #! NotImplemented
    """
    Deletes the entry of a job in the Database.
    Redirects to show_jobs
    """
    Job.delete(id)
    return redirect(url_for('show_jobs'))

@app.route('/jobs/read/<id>',methods = [GET])
def read_job(id: int):
    """
    Shows the information about a Job
    """
    print(id)
    return render_template('jobs_r.html',
                           values = Job.read_as_dict(id))

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
        Job.update(
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
    
    
    return render_template(
        'jobs_u.html',
        jobs = JobID.read_as_dict(id),
        data = Job.read_as_dict(id),
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
        Job.create(
            company = jq.COMPANY,
            description = jq.DESCRIPTION,
            mail = jq.MAIL,
            phone_number = jq.PHONE_NUMBER,
            state_id = jq.STATE,
            title_id = jq.TITLE_ID,
            url = jq.URL
        )
        f = Job.get_last()
        print(f)
        return redirect(f'read/{f}')
    
    
    return render_template(
        'jobs_c.html',
        jobs = JobID.read_all(),
        states = JobApplianceStates.get()
        ), 200

@app.route('/jobs',methods = [GET])
def show_jobs():
    """
    Shows all jobs, listed in the database.
    * Fix the id problem(ID -> Text Translation)
    """
    return render_template('jobs_s.html',
                           jobs=Job.read_all())