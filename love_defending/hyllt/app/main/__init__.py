# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:48

author @heyao
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
