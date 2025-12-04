from jinja2 import Template
from src.flask_main import url_for
PATH = "./src/backend/cv_creator/"
from src.backend.cv_creator.objects import *

def generate(filepath: str, settings: str) -> str:
    # Reading
    loc = {}
    exec(settings, globals(), loc)
    with open(f'{PATH}index.html', 'rb') as f:
        HTML = f.read().decode()
        
    with open(f'{PATH}styles.css', 'rb') as f:
        CSS = f.read().decode()
    # Rendering
    template = Template(HTML)
    pp = url_for('static', filename='profile.png')
    result = template.render(
        data = loc['CVC'], 
        enumerate = enumerate, 
        css = CSS,
        profile_path = pp
    )
    del loc['CVC']
    # Writing & Return
    #with open(filepath, 'wb') as f:
    #    f.write(result.encode())
        
    return result