from src.backend.flask_main import *
from src.data import JOBS, JOBIDS, LJOBS, CVCS, JobApplianceStates
from typing import Callable
from jinja2 import Template
import io
from json import dumps
from src.cv_creator.cv_generator import generate


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
    jobs = JOBS.read_all(True, JOBIDS)
    l = len(jobs)
    return render_template('jobs_s.html',
                           jobs=jobs,
                           ammount = l)
    
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
    
@app.route('/export/json',methods = [GET])
def export_json():
    """
    Downloads the jobs-database as json.
    """
    return jsonify(JOBS.read_all(True, JOBIDS))

@app.route('/export/csv',methods = [GET])
def export_csv():
    """
    Downloads the jobs-database as csv.
    """
    TABLE = []
    for entry in JOBS.read_all(True, JOBIDS):
        TABLE.append('|'.join([str(entry[key]) for key in entry if key not in ('description', 'state_id', 'job_id', 'id')]))
    return send_file(
        io.BytesIO("\n".join(TABLE).encode()),
        download_name= 'JobApplicationSummary.csv'
    )

@app.route('/summary',methods = [GET, POST])
def summary():
    if request.method.upper() == POST:
        from ai_api import improve_writing
        return improve_writing(request.form.get('text'))
    
    
    return render_template(
        'summary_writer.html',
    )
    
@app.route('/linkedin',methods = [GET])
def linkedin_show(): 
    all_jobs = LJOBS.read_all(True)
    return render_template('linkedin_job_viewer.html', data = all_jobs, ammount = len(all_jobs))

@app.route('/linkedin/create',methods = [GET, POST])
def linkedin_create():
    if request.method.upper() == POST:
        files = request.files.getlist('file')
        print(files)
        from src.linkedin_job_search_fetch import fetch_job_ids, fetch_linkedin_job_data
        all_jobs = []
        for file in files:
            data = file.stream.read().decode()
            jobs = fetch_job_ids(data)
            all_jobs.extend([fetch_linkedin_job_data(id) for id in jobs])
        for job in all_jobs:
            print(job)
            LJOBS.create(**job)
            print(LJOBS.read(-1))
        # Store all jobs from linkedIn into the database
        return redirect(url_for('linkedin_show'))
    return render_template(
        'linkedin_job_getter.html'
    )

@app.route('/load',methods = [GET])
def load():
    return render_template(
        'load.html'
    )

@app.route('/cv/create',methods = [GET, POST])
def cv_create():
    if request.method.upper() == POST:
        files = request.files.getlist('cvcs')
        print(files)
        for file in files:
            name = file.filename.split('.', maxsplit=1)[0]
            cvc = file.stream.read()
            CVCS.create(cvc, name)
                
        return redirect(url_for('cv_read',id=-1))
    return render_template(
        'cv_c.html'
    )

@app.route('/cv/read/<id>',methods = [GET])
def cv_read(id: int):
    cvc = CVCS.read(id)
    cvc = generate(f'{cvc.name}.html', cvc.cvc)
    return cvc

@app.route('/cv/delete/<id>',methods = [POST])
def cv_delete(id: int):
    CVCS.delete(id)
    return redirect(url_for('cv_show'))

@app.route('/cv',methods = [GET])
def cv_show():
    cvs = CVCS.read_all()
    return render_template(
        'cv_s.html',
        cvs = cvs,
        ammount = len(cvs)
    )

@app.route('/license',methods = [GET])
def license():
    with open('LICENSE') as f:
        LICENSE = f.read()
    return render_template(
        'license.html',
        license = LICENSE
    )