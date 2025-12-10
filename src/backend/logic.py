from src.flask_main import *
from src.backend.data import JOBS, JOBIDS, LJOBS, CVCS, JobApplianceStates, file_read, create_file_if_not_exist, file_write
from typing import Callable
from jinja2 import Template
import io
from json import dumps, loads
from src.backend.cv_creator.cv_generator import generate
from src.backend.linkedin_job_search_fetch import fetch_job_ids, fetch_linkedin_job_data, get_tags, get_mails, get_phone_number
from src.backend.search import linkedin_search
from src.constants import HELP
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
    Shows the information about a single Job
    redirect to itself with data id if data id is not input
    """
    data = JOBS.read_as_dict(id, JOBIDS)
    if data is None: return "Error occured"
    
    if str(data['id']) != str(id):
        return redirect(url_for(f'read_job',id=data['id']))
    
    return render_template('jobs_r.html',
                           values = JOBS.read_as_dict(id, JOBIDS), tags = get_tags(data['description']))

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
    """
    For creating a new Job-title in the Database
    
    GET:
        Let the user create a new job-title
    POST:
        Adds the Job-title to the Database
        Redirects to job_titles/read/-1
    """
    
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
    
@app.route('/linkedin',methods = [GET, POST])
def linkedin_show(): 
    print(request.query_string)
    q = {}
    if request.query_string:
        q = {q.split('=')[0]: q.split('=')[1] for q in request.query_string.decode().split('&')}
    if q.get('fast'):
        all_jobs = [j for j in LJOBS.read_all(True) if j['fast']]
    else:
        all_jobs = LJOBS.read_all(True)
    all_jobs_length = len(all_jobs)
    tags = [get_tags(job['description']) for job in all_jobs]
    
    t = request.form.get('search','').lower()
    all_jobs, tags = linkedin_search(t, all_jobs, tags)

    return render_template('linkedin_job_viewer.html', data = all_jobs, ammount = len(all_jobs),max_ammount = all_jobs_length, tags = tags, zip = zip, searchfor=t)

@app.route('/linkedin/create',methods = [GET, POST])
def linkedin_create():
    if request.method.upper() == POST:
        
        files = request.files.getlist('file')
        all_jobs = []
        data = files[0].stream.read().decode()
        jobs = fetch_job_ids(data)
        all_jobs.extend([fetch_linkedin_job_data(id) for id in jobs])
        for job in all_jobs:
            if job.get('error') is not None: 
                print(job['error'])
                continue
            LJOBS.create(**job)
        return redirect(url_for('linkedin_show'))
    return render_template(
        'linkedin_job_getter.html'
    )

@app.route('/linkedin/read/<id>',methods = [GET])
def linkedin_read(id: int): 
    data = LJOBS.read_as_dict(id)
    return render_template('linkedin_job_r.html', data = data, tags = get_tags(data['description']))

@app.route('/linkedin/delete/<id>',methods = [GET])
def linkedin_delete(id: int): 
    LJOBS.delete(id)
        
    return redirect(url_for('linkedin_show'))

@app.route('/load',methods = [GET])
def load():
    return render_template(
        'load.html'
    )

@app.route('/cv/create',methods = [GET, POST])
def cv_create():
    if request.method.upper() == POST:
        f = request.form
        name = f.get('name')
        profession = f.get('profession')
        summary = f.get('summary')
        if not name or not profession or not summary:
            return "Not all values are set"
        
        if not os.path.isfile('./settings/preset.py'):
            return "You have not defined a preset -> insert a cvc preset in ./settings/preset.py."
        with open('./settings/preset.py','rb') as f:
            preset = f.read().decode()
            
        content = preset.replace('__SUMMARY__',f'{summary}').replace('__PROFESSION__', f'{profession}')

        CVCS.create(content, name)
        
        return redirect(url_for('cv_read',id=-1))
    return render_template(
        'cv_c.html', jobs = JOBIDS.read_all(True)
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

@app.route('/help',methods = [GET])
def help_show():
    
    return render_template(
        'help.html',
        help = HELP
    )
    
@app.route('/create_by_linkedin/<id>',methods = [POST])
def create_job_from_linkedin(id: int):
    """
    company: str, 
    title_id: int, 
    url: str, 
    mail: str, 
    phone_number: str, 
    description: str, 
    state_id: int
    
    edge cases:
        - job-title does not exist
        
    """
    data = LJOBS.read_as_dict(id)
    if data is None: return "no data"
    if data.get('alreadyinjobs') is not None:
        return "already in jobs"
    # Job title assign
    job_exist = JOBIDS.get_job_exist(data['job_title'])
    if not job_exist:
        JOBIDS.create(data['job_title'])
        job_exist = JOBIDS.get_job_exist(data['job_title'])

    mails = get_mails(data['description'])
    phone_numbers = get_phone_number(data['description'])
    
    mails = mails[-1] if mails else None
    phone_numbers = phone_numbers[-1] if phone_numbers else None
    
    new_jobs = {
        'company' : data['company'],
        'description': data['description'],
        'url': f'https://www.linkedin.com/jobs/view/{data["lid"]}',
        'mail': mails,
        'phone_number': phone_numbers,
        'title_id': job_exist,
        'state_id': JobApplianceStates.APPLIED
    }
    
    print(new_jobs)
    data['alreadyinjobs'] = True
    LJOBS.update(**data)
    
    
    JOBS.create(**new_jobs)
    
    return redirect(url_for('read_job',id="-1"))

@app.route('/jobsearch_settings',methods = [GET])
def jobsearch_settings():
    
    return render_template(
        'jobsearch_settings.html'
    )
    
@app.route('/jobsearch_settings_as_json',methods = [GET, POST])
def jobsearch_settings_as_json():
    if request.method.upper() == POST:
        files = request.files.getlist('file')
        print(files)
        data = files[0].stream.read().decode()
        print(data)

        cleaned_tags = [",".join([tag for tag in tags.split(',') if tag]) for tags in data[2:-1].split(';')]
        print(cleaned_tags)
        cleaned_tags = ";".join(cleaned_tags)
        
        print(cleaned_tags)
        file_write('./settings/jobsearch_settings.json', cleaned_tags)
        return 'finished writing', 202
    
    create_file_if_not_exist('./settings/jobsearch_settings.json', '[[],[],[]]')
    data = file_read('./settings/jobsearch_settings.json')
    #res = ";".join([",".join([tag for tag in taglist]) for taglist in data])
    return data

@app.route('/aiiw',methods = [POST])
def ai_improve_writing():
    if request.method.upper() == POST:
        print(request.form)
        from ai_api import improve_writing
        r = improve_writing(request.form['text'])
        if r is None: return {'text': ''}
        return jsonify({'text': r})
    #return render_template('cv_ai.html')
