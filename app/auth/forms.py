from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from .. models import  User
from wtforms import ValidationError



class RegistrationForm(Form):

    # userInfo = {}
    # userInfo = Form
    # email = userInfo.get('email')
    # print('email')

    email = StringField('email', validators=[Required()])
    business = StringField('business', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            print("Email already registered.")
            # self.email.errors.append(('Email already registered'))
            raise ValidationError('Email already registered.')


class Registration2Form(Form):
    firstName = StringField('firstName', validators=[Required()])
    title = StringField('title', validators=[Required()])
    zipCode = StringField('zipCode', validators=[Required()])
    skills = StringField('skills', validators=[Required()])
    bizDesc = StringField('bizDesc', validators=[Required()])
    employeeNumber = StringField('employeeNumber', validators=[Required()])

class LoginForm(Form):
    email = StringField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


