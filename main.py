from src.flask_main import *
from src.backend.logic import *
GET, POST, DELETE = 'GET', 'POST', 'DELETE'

def err_return(code: int = 404):
    """
    Returns a simple template for debugging purposes.
    """
    return render_template('error.html', err=code, msg=http_status_codes[code]), code

@app.route('/',methods = [GET])
def index():
    """
    Index redirects to /Jobs
    """
    return redirect('/jobs')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)