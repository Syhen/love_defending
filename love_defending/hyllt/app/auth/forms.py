# -*- coding: utf-8 -*-
"""
Created on 2017/05/17 13:00:25

@author: mac
"""

from flask_wtf import FlaskForm as Form
from wtforms.validators import DataRequired as Required
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.validators import Length, EqualTo


class LoginForm(Form):
    name = StringField('用户名', validators=(Required(message='请输入用户名'), Length(1, 64)))
    password = PasswordField('密码', validators=(Required(message='请输入密码'),))
    key = HiddenField(id='key')
    pubkey = HiddenField(id='pubkey')
    submit = SubmitField('登录')


class RegisterForm(Form):
    name = StringField('用户名', validators=(Required(message='请输入用户名'), Length(1, 64)))
    password = PasswordField('密码', validators=(Required(message='请输入密码'), Length(1, 64)))
    role = SelectField('用户权限', validators=(Required(message='请选择用户角色'),), choices=[(2, 'user'), (1, 'admin')],
                       coerce=int)
    submit = SubmitField('注册')


class ModifyPasswordForm(Form):
    original_password = PasswordField('请输入旧密码', validators=(Required(message='请输入密码'), Length(1, 64)))
    password = PasswordField('请输入新密码',
                             validators=(Required(message='请输入新密码'),
                                         Length(1, 64),
                                         EqualTo('ensure_password', message='两次输入的密码必须相同')))
    ensure_password = PasswordField('请再次输入密码', validators=(Required(message='请输入密码'), Length(1, 64)))
    submit = SubmitField('修改密码')
