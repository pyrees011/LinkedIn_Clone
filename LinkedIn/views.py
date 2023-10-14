from flask import Blueprint, render_template, current_app, request
from flask_login import login_required, current_user
from .mongo import jobs

views = Blueprint("views", __name__)

@views.route('/')
@login_required
def homepage():
    job_details = list(jobs.find())
    return render_template('homepage.html', job_details=job_details)

