# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:38

author @heyao
"""

from flask import Flask

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

from config import config

admin = Admin()
bootstrap = Bootstrap()
mongodb = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app)
    bootstrap.init_app(app)
    mongodb.init_app(app, config_prefix='MONGO')

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
