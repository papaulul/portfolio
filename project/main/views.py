from datetime import datetime 
from flask import render_template, session, redirect, url_for
from . import main 

@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html' ,current_time=datetime.utcnow())

@main.route('/airbnb')
def airbnb():
    return render_template('airbnb_about.html')

@main.route('/airbnb/about')
def airbnb_about():
    return render_template('airbnb_about.html')

@main.route('/glassdoor')
def glassdoor():
    return render_template('glassdoor.html')
@main.route('/glassdoor/about')
def glassdoor_about():
    return render_template('glassdoor.html')

@main.route('/tripadvisor')
def tripadvisor():
    return render_template('tripadvisor.html')

@main.route('/tripadvisor/about')
def tripadvisor_about():
    
    return render_template('tripadvisor.html')
