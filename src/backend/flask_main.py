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

from src.errors import  http_status_codes
app = Flask(__name__)