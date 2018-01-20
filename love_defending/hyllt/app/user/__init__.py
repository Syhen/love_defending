# -*- coding: utf-8 -*-
"""
create on 2018-01-20 下午8:14

author @heyao
"""

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views
