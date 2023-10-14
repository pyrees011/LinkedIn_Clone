from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import request, jsonify, render_template, Blueprint, redirect, current_app, url_for, flash
from flask_login import current_user, login_required
import random
from datetime import datetime
import os
from werkzeug.utils import secure_filename


mongo = Blueprint('mongo', __name__)


uri = "mongodb+srv://RaunakBhansali:951203@cluster0.reeyyqp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['acoount']
application = db['application']
jobs = db['jobs']
profile_details = db['profile']
# user = db['users']


@mongo.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == "POST":
        image = request.files['profile_image']
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['PROFILE'], image_filename))

        profile_info = {
            'username' : current_user.username,
            'email' : current_user.email,
            'contact' : request.form['contact'],
            'location' : request.form['location'],
            'image' : image_filename,
        }

        profile_doc = profile_details.find_one({'username' : current_user.username})

        if profile_doc:
            profile_details.update_one(
                {'username' : current_user.username},
                {'$push' : {'profile_info' : profile_info}}
            )
        else:
            new_profile = {
                'username' : current_user.username,
                'profile_info' : [profile_info]
            }
            profile_details.insert_one(new_profile)
        return redirect(url_for('views.homepage'))
    return render_template('profile.html')



@mongo.route('/createJobs', methods=['POST', 'GET'])
@login_required
def createJobs():
    user_id = current_user.id
    if request.method == "POST":

        profile_doc = profile_details.find_one({'username' : current_user.username})
        if profile_doc:
            profile_info = profile_doc['profile_info']
            for info in profile_info:
                profile_filename = info['image']
        else:
            profile_filename = "default_profile.avif"

        image = request.files['image']
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        job_info = {
            'job_id' : random.randint(1, 100000),
            'job_title' : request.form['jobTitle'],
            'companyName' : request.form['companyName'],
            'location' : request.form['location'],
            'jobDesc' : request.form['jobDesc'],
            'salaryRange' : request.form['salaryRange'],
            'duration' : request.form['duration'],
            'requirements' : request.form['requirements'],
            'image' : image_filename,
            'profile_image' : profile_filename,
            'username' : current_user.username,
            'email' : current_user.email,
        }
        jobs_doc = jobs.find_one({'user_id' : user_id})

        if jobs_doc:
            jobs.update_one(
                {'user_id' : user_id},
                {'$push' : {'job_info' : job_info}}
            )

        else:
            new_job = {
                'user_id' : user_id, 
                'job_info' : [job_info]
            } 
            jobs.insert_one(new_job)

        return redirect(url_for('views.homepage'))
    return render_template('createJobs.html')


@mongo.route('/applications/<int:job_id>', methods=['POST', 'GET'])
@login_required
def applications(job_id):
    user_id = current_user.id
    if request.method == "GET":

        jobs_doc = list(jobs.find())
        for jobInfo in jobs_doc:
            job_info = jobInfo['job_info']
            for job in job_info:
                if job['job_id'] == job_id:
                    job_title = job['job_title']
                    company_name = job['companyName']
                    salary_range = job['salaryRange']
                    duration = job['duration']
                    username = job['username']
                    image = job['image']
                    email = job['email']

        appl = {
            'job_id' : job_id,
            'job_title' : job_title,
            'company_name' : company_name,
            'salary_range' : salary_range,
            'duration' : duration,
            'employer' : username,
            'employee_email' : current_user.email,
            'employee' : current_user.username,
            'email' : email,
            'image' : image,
        }

        application_doc = application.find_one({ 'user_id' : user_id })

        if application_doc:
            application.update_one(
                {'user_id' : user_id},
                {'$push' : {'appl_details' : appl}}
            )

        else:
            new_appl = {
                'user_id' : user_id,
                'appl_details' : [appl]
            } 

            application.insert_one(new_appl)
        return redirect(url_for('views.homepage'))
    

@mongo.route('/viewApplications', methods=['POST', 'GET'])
@login_required
def viewApplications():
    user_id = current_user.id
    appl_details = application.find_one({ 'user_id' : user_id})
    if appl_details:
        appl = appl_details['appl_details']
    else:
        appl = []
    return render_template('viewApplications.html', appl = appl)


@mongo.route('/deletejob/<int:job_id>', methods=['DELETE', 'GET'])
@login_required
def deleteCart(job_id):
    user_id = current_user.id
    result = jobs.update_one(
        {'user_id': user_id},
        {'$pull': {'job_info': {'job_id': job_id}}}
    )
    if result.modified_count == 1:
        # return redirect(url_for('blogs.getblogs'))
        return jsonify({ 'message' : 'task deleted successfully' })
    else:
        return jsonify({ 'message' : 'task not found'}), 404


# @mongo.route('/updateJobs/<int:job_id>', methods=['PUT', 'POST', 'GET'])
# def updateQuantity(job_id):
#     user_id = current_user.id
#     if request.method == 'POST':
#         result = jobs.update_one(
#             {'user_id': user_id, 'job_info.job_id': job_id},
#             {'$set': {
#                 'cart_items.$.quantity': updatedQuantity  # Use '$' here to update the correct item
#             }})

#         if result.modified_count == 1:
#             # return redirect(url_for('blogs.getblogs'))
#             return jsonify({'message' : 'task updated successfully'})
#         else:
#             return jsonify({ 'message' : 'task not found'}), 404
        

