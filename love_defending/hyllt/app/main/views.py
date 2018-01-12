# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:48

author @heyao
"""

import sys

import math
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from . import main
from .. import mongodb

reload(sys)
sys.setdefaultencoding('utf-8')


class Pagination(object):
    def add_arg(self, name, value):
        setattr(self, name, value)


def generate_video_list(videos, page, pagesize=20):
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
    return pagination, videos


@main.route('/video/<type>/<page>')
@login_required
def videos(type='total', page=1):
    page = int(page)
    pagesize = 20
    sort_key = dict(
        total='total_views',
        day='views_per_day',
        date='date'
    )[type]
    videos = mongodb.db['video_list'].find().sort([('read_status', 1), (sort_key, -1)])
    pagination, videos = generate_video_list(videos, page, pagesize)
    return render_template('love_defending.html', videos=videos, pagination=pagination, page=page, type=type)


@main.route('/video/mark/<video_id>/<page>/<status>')
@login_required
def video_mark(video_id, page, status=1):
    status = int(status)
    if status != 0 and status != 1:
        flash("失败")
    mongodb.db['video_list'].update(
        {'_id': video_id},
        {'$set': {'read_status': status}}
    )
    return redirect(url_for('main.videos', page=page, type='total'))


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/video/<type>/<keyword>/<page>')
@login_required
def search_video(type='total', keyword='', page=1):
    page = int(page)
    pagesize = 20
    sort_key = dict(
        total='total_views',
        day='views_per_day',
        date='date'
    )[type]
    videos = mongodb.db['video_list'].find({'title': {'$regex': keyword}}).sort([('read_status', 1), (sort_key, -1)])
    pagination, videos = generate_video_list(videos, page, pagesize)
    return render_template('love_defending.html', videos=videos, pagination=pagination, page=page, type=type)
