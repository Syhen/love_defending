# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:48

author @heyao
"""

import sys

import math
from flask import render_template, flash, redirect, url_for

from . import main
from .. import mongodb

reload(sys)
sys.setdefaultencoding('utf-8')


class Pagination(object):
    def add_arg(self, name, value):
        setattr(self, name, value)


@main.route('/video/<page>')
def videos(page=1):
    page = int(page)
    pagesize = 20
    videos = mongodb.db['video_list'].find().sort([('read_status', 1), ('total_views', -1)])
    total_items = videos.count()
    videos_info = videos.skip((page - 1) * pagesize).limit(pagesize)
    videos = []
    for video in videos_info:
        video['total_views'] = str(video['total_views'] / 10000) + u'万'
        video['full_title'] = video['title']
        video['title'] = video['title'][:14] + '…' if len(video['title']) > 14 else '{0:　<14}'.format(video['title'])
        videos.append(video)
    pages = int(math.ceil(total_items * 1. / pagesize))

    def get_info():
        max_page = pages + 1
        for i in range(max(1, page - 4), min(max_page, max(1, page - 4) + 10)):
            yield i

    pagination = Pagination()
    pagination.add_arg('has_prev', page != 1)
    pagination.add_arg('page', page)
    pagination.add_arg('iter_pages', get_info)
    pagination.add_arg('has_next', (total_items / pagesize) > page)
    pagination.add_arg('pages', pages)
    return render_template('love_defending.html', videos=videos, pagination=pagination, page=page)


@main.route('/video/mark/<video_id>/<page>/<status>')
def video_mark(video_id, page, status=1):
    status = int(status)
    if status != 0 and status != 1:
        flash("失败")
    mongodb.db['video_list'].update(
        {'_id': video_id},
        {'$set': {'read_status': 1}}
    )
    return redirect(url_for('main.videos', page=page))


@main.route('/')
def index():
    return render_template('index.html')
