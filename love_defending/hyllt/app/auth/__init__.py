# -*- coding: utf-8 -*-
"""
Created on 2017/05/17 12:59:59

@author: mac
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
