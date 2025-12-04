from flask import Flask,jsonify, render_template, request, redirect, url_for, send_file
from flask import Request
from src.constants import  http_status_codes, GET, POST, DELETE
import os

directory = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
directory = os.path.join(directory, 'Application-Manager', 'src', 'frontend')

app = Flask(__name__,static_folder=directory + '\\static', template_folder=directory + '\\templates')