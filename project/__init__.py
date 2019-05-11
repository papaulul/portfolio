from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
from config import config 
from flask_moment import Moment

bootstrap = Bootstrap()
moment= Moment()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    bootstrap.init_app(app)
    moment.init_app(app)
    return app