from flask import Flask,jsonify, render_template, request, redirect
from src.data import get_jobs, get_job_id
from src.errors import  http_status_codes
app = Flask(__name__)

GET, POST = 'GET', 'POST'

def err_return(code: int = 404):
    return render_template('error.html', err=code, msg=http_status_codes[code]), code

class JobQuery:
    def __init__(self, query: list[str]):
        
        duery = {k.split('=',maxsplit=1)[0]: k.split('=',maxsplit=1)[1] for k in query}
        self.COMPANY = duery['company']
        self.TITLE_ID = int(duery['job_title'])
        self.URL = duery['url']
        self.MAIL = duery['mail']
        self.PHONE_NUMBER = duery['phone_number']
        self.DESCRIPTION = duery['description']
        self.STATE = int(duery['state'])
        
        
@app.route('/jobs/create',methods = [GET, POST])
def create_job():
    if request.method.upper() == POST:
        print(request.query_string.decode().split('&'))
        #+ Add Job to DB
        return 'Nothing here', 403
    
    
    return render_template(
        'jobs_cud.html',
        jobs = get_jobs()
        ), 200

@app.route('/',methods = ['GET'])
def user_login():
    return err_return(501)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)