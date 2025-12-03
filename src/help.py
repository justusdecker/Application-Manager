import markdown
from html.parser import HTMLParser
from src.constants import HELP
        
def generate_help() -> str:
    return HELP