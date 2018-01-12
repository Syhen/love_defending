# -*- coding: utf-8 -*-
"""
Created on 2017/05/17 12:36:23

@author: mac
"""

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Permission(object):
    VIEW_MKT = 0x01
    VIEW_ALL = 0x02
    ADMIN = 0x07


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(16), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.INTEGER, db.ForeignKey('roles.id'), default=Permission.VIEW_ALL, nullable=False)

    @property
    def password(self):
        raise ValueError('can\'t get password.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        return self.role is not None and (self.role.permission & permission) == permission

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return r'<User {0}>'.format(self.name)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(16))
    permission = db.Column(db.INTEGER, default=Permission.VIEW_ALL)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __unicode__(self):
        return r'<Role {name}>'.format(name=self.name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
