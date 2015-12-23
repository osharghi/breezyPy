from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from . import login_manager
from datetime import datetime
import os

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        print("creating roles")
        roles = {
            'User': (Permission.FOLLOW |
                      Permission.COMMENT |
                      Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                           Permission.COMMENT |
                           Permission.WRITE_ARTICLES |
                           Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)

        }
        print("About to insert roles")
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            print("Done inserting roles")
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    business_name = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    firstName = db.Column(db.String(128))
    title = db.Column(db.String(64))
    zipAddress = db.Column(db.String(64))
    employeeNumber = db.Column(db.String(64))
    bizDesc = db.Column(db.Text)
    skills = db.relationship('Skill', backref='author', lazy='dynamic')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BREEZY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                print("setting role")
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        print(self.password_hash)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register_fromJSON(json_register):

        userInfo = {}
        userInfo = json_register.get('userInfo')
        email = userInfo.get('email')
        business = userInfo.get('business')
        password = userInfo.get('password')
        # email = json_register.get('email')
        # business = json_register.get('business')
        # password = json_register.get('password')
        if email is None or email == '' or business is None or business == '' or password is None or password == '':
            return "missing User Information"
            # raise ValidationError('Missing User information')
        return User(email=email, business_name=business, password_hash=generate_password_hash(password))


    def __repr__(self):
        return '<User %r>' % self.email

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    skillTitle = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))