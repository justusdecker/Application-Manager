from flask import Flask,jsonify, render_template, request, redirect, url_for, send_file
from flask import Request
GET, POST, DELETE = 'GET', 'POST', 'DELETE'

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

from src.constants import  http_status_codes
import os
directory = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
directory = os.path.join(directory, 'Application-Manager', 'src', 'frontend')

print(directory)
app = Flask(__name__,static_folder=directory + '\\static',template_folder=directory + '\\templates')