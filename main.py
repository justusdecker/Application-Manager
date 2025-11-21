from flask import Flask,jsonify, render_template, request, redirect
from src.data import JobsTable, JobIdsTable, JobID, Job
from src.errors import  http_status_codes
app = Flask(__name__)

GET, POST, DELETE = 'GET', 'POST', 'DELETE'

def err_return(code: int = 404):
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

@app.route('/jobs/delete/<id>',methods = [DELETE, GET])
def delete_job(id: int):
    print(id)
    return redirect('jobs_r.html')

@app.route('/jobs/read/<id>',methods = [GET])
def read_job(id: int):
    print(id)
    return render_template('jobs_r.html',
                           values = Job.get_job_info(id))

@app.route('/jobs/create',methods = [GET, POST])
def create_job():
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
        'jobs_cu.html',
        jobs = JobID.get_job_ids()
        ), 200

@app.route('/',methods = [GET])
def index():
    return err_return(501)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)