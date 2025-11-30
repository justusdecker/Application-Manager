from jinja2 import Template
from src.cv_creator.cvc import CVC
PATH = "./src/cv_creator/"

def generate(filepath: str, settings = CVC) -> str:
    # Reading
    with open(f'{PATH}index.html', 'rb') as f:
        HTML = f.read().decode()
        
    with open(f'{PATH}styles.css', 'rb') as f:
        CSS = f.read().decode()
    # Rendering
    template = Template(HTML)
    result = template.render(
        data = settings, 
        enumerate = enumerate, 
        css = CSS
    )
    # Writing & Return
    with open(filepath, 'wb') as f:
        f.write(result.encode())
        
    return result