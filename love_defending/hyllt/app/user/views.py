# -*- coding: utf-8 -*-
"""
create on 2018-01-20 下午8:19

author @heyao
"""
from flask import render_template
from flask_login import login_required

from app import mongodb
from app.main.views import generate_video_list
from . import user


@user.route('/video/<type>/<page>')
@login_required
def videos(type='total', page=1):
    page = int(page)
    pagesize = 20
    sort_key = dict(
        total='total_views',
        day='views_per_day',
        date='date'
    )[type]
    videos = mongodb.db['video_list'].find({'collect': 1}).sort([('read_status', 1), (sort_key, -1)])
    pagination, videos = generate_video_list(videos, page, pagesize)
    return render_template('user/info.html', videos=videos, pagination=pagination, page=page, type=type)
