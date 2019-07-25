import os 
from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
from config import config 
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, session, redirect, url_for
from datetime import datetime 

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment= Moment()
db = SQLAlchemy()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html' ,current_time=datetime.utcnow())

@app.route('/airbnb')
def airbnb():
    return render_template('airbnb_about.html')

@app.route('/airbnb/about')
def airbnb_about():
    return render_template('airbnb_about.html')

@app.route('/airbnb/analysis')
def airbnb_analysis():
    return render_template('airbnb_about.html')

@app.route('/airbnb/demo')
def airbnb_demo():
    return render_template('airbnb_about.html')


@app.route('/glassdoor')
def glassdoor():
    return render_template('glassdoor_about.html')
@app.route('/glassdoor/about')
def glassdoor_about():
    return render_template('glassdoor_about.html')
@app.route('/glassdoor/analysis')
def glassdoor_analysis():
    return render_template('glassdoor_about.html')

@app.route('/glassdoor/demo')
def glassdoor_demo():
    return render_template('glassdoor_about.html')

@app.route('/tripadvisor')
def tripadvisor():
    return render_template('tripadvisor_about.html')

@app.route('/tripadvisor/about')
def tripadvisor_about():
    return render_template('tripadvisor_about.html')

@app.route('/tripadvisor/analysis')
def tripadvisor_analysis():
    return render_template('tripadvisor_analysis.html')

@app.route('/tripadvisor/demo', methods=['GET','POST'])
def tripadvisor_demo():
    return render_template('tripadvisor_demo.html')

@app.route('/aboutme')
def aboutme():
    return render_template(('aboutme.html'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
if __name__ =='__main':
        app.run()