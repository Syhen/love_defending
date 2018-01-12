# -*- coding: utf-8 -*-
"""
Created on 2017/05/17 13:00:07

@author: mac
"""

from flask import render_template, flash, redirect, url_for, abort, request, session

from flask_login import logout_user, login_user, current_user, login_required
from . import auth
from .forms import LoginForm, RegisterForm, ModifyPasswordForm
from ..models import User
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = User.query.filter_by(name=name).first()
        if user:
            if user.verify_password(password):
                flash('登录成功。')
                login_user(user, True)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('密码错误。')
        else:
            flash('用户不存在。')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin():
        abort(403)
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(name=name).first()
        if user:
            flash('该用户名已存在。')
            return redirect(url_for('auth.register'))
        else:
            user = User(
                name=name,
                password=form.password.data,
                role_id=int(form.role.data)
            )
            db.session.add(user)
            db.session.commit()
            form.name.data = ''
            flash('注册成功。')
    return render_template('auth/register.html', form=form)


@auth.route('/modify', methods=['GET', 'POST'])
@login_required
def modify():
    form = ModifyPasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.original_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            pop_list = ['privatekey', 'key']
            [session.pop(key) for key in pop_list if key in session]
            flash('密码修改成功。你的登录信息发生修改，请重新登录。')
            return redirect(url_for('auth.logout'))
        else:
            flash('旧密码错误，请重新验证。')
            return redirect(url_for('auth.modify'))
    return render_template('auth/modify_password.html', form=form)
