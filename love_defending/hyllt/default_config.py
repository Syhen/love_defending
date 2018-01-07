# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午9:41

author @heyao
"""

import os


class Config(object):
    HOST = '0.0.0.0'
    PORT = 2117
    SECRET_KEY = os.environ.get("LD_SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass
