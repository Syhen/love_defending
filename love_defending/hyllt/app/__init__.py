# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:38

author @heyao
"""

from flask import Flask

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from config import config

admin = Admin(template_mode='bootstrap3')
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mongodb = PyMongo()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录。'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app)
    bootstrap.init_app(app)
    mongodb.init_app(app, config_prefix='MONGO')
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
