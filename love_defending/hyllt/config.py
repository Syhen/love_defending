# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:39

author @heyao
"""

from default_config import Config
from production_config import ProductionConfig


class DevelopmentConfig(Config):
    DEBUG = True

    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_DBNAME = 'love_defending'
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''

    LOG_PATH = '/Users/heyao/love_defending.log'


config = dict(
    default=DevelopmentConfig,
    development=DevelopmentConfig,
    production=ProductionConfig
)
