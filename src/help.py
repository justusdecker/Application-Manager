import markdown
from html.parser import HTMLParser
HELP = {
    'Help': {
        'Jobs': [
            "You can create a job here",
            "You need to insert a few values here:",
            "* Company-name(*)",
            "* job-title(*): The job-title / profession of the job you are looking for(If a job-title not exists you need to create it first in job-titles/create",
            "* url(*): The url of the job you are looking",
            "* mail: The mail-address of the company",
            "* phone-number: The phone-number of the company",
            "* description: The description of the job you are looking for"
        ],
        'Job Ids': [
            "You can create a job-id / profession here",
            "This is used for Jobs"
        ]
    }
}
        
def generate_help() -> str:
    return HELP