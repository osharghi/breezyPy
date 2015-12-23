from . import auth
import app
from config import config
import os
from flask import redirect, request, url_for, flash, jsonify, current_app, send_from_directory
from werkzeug.datastructures import MultiDict
from forms import RegistrationForm, Registration2Form, LoginForm
from . import forms
import flask
from .. models import User, Skill
from .. import db
from flask.ext.login import logout_user, login_required, login_user, current_user


@auth.route('/register1', methods=['POST'])
def register1():
    print("Hello")
    try:
        print('HERE')

        # data = MultiDict(mapping=request.json)
        d=MultiDict(mapping=request.json)
        print(d)
        data = d.get('userInfo')
        data2 = MultiDict(mapping=data)
        print(data2)
        form = RegistrationForm(data2)

        if form.validate():
            print("form valid")
            print(form.email.data)
            print(form.password.data)
            print(form.business.data)
            user = User.register_fromJSON(request.json)
            print('adding user')
            db.session.add(user)
            db.session.commit()
            login_user(user, False)
            return jsonify({'response' : user.id})
        else:
            print("fail")
            if form.email.errors:
                print('Email error')
                return jsonify({'error' : form.email.errors[0]})

    except Exception:
        print('oops')
        return jsonify({'response': 'trouble'})

        # return jsonify({'Unable_To_Access_SignUp_Error': 'Unable to access signup.'})

@auth.route('/register2', methods=['POST'])
def register2():
    print('hello2')
    try:
        print('hello3')

        # data = MultiDict(mapping=request.json)
        # form = Registration2Form(data)
        d = MultiDict(mapping=request.json)
        print(d)
        data = d.get('userInfo')
        data2 = MultiDict(mapping=data)
        print(data2)
        form = Registration2Form(data2)
        print('hello4')


        # if form.validate():
        print('form2 valid')
        print(form.firstName.data)
        print(form.title.data)
        print(form.zipCode.data)
        print(form.skills.data)
        print(form.bizDesc.data)
        print(form.employeeNumber.data)
        current_user.firstName = form.firstName.data
        current_user.title = form.title.data
        current_user.zipAddress = form.zipCode.data
        current_user.employeeNumber = form.employeeNumber.data
        current_user.bizDesc = form.bizDesc.data
        skillList = form.skills.data.split('#')
        skills = filter(None, skillList)
        print(skills)
        for skill in skills:
            if skill != '':
                print('SKILL TO ADD %s' % skill)
                skillToAdd = Skill(skillTitle=skill, author=current_user._get_current_object())
                print('heretest1')
                db.session.add(skillToAdd)
                print('heretest2')
        print('adding user')
        db.session.add(current_user)
        db.session.commit()
        userInfo = {'email':current_user.email, 'name':current_user.firstName, \
                    'title': current_user.title, 'company': current_user.business_name, 'zipcode': current_user.zipAddress, \
                    'employeeNumber': current_user.employeeNumber, 'bizDesc': current_user.bizDesc}
        return jsonify({'response' : userInfo})
    except Exception:
        print('oops')
        return jsonify({'response': 'trouble'})


@auth.route('/search/<skill>', methods=['GET'])
def search(skill):
    print('reached search')
    if request.method == 'GET':
        print('GETTING')
        try:
            print('trying')
            print(skill)
            queriedSkills = Skill.query.filter_by(skillTitle=skill)
            someList=[]
            if queriedSkills != None:
                print('now we here1')
                print(queriedSkills)
                print('now we here2')
                for skill in queriedSkills:
                    print(skill.author_id)
                    userID = skill.author_id
                    user = User.query.filter_by(id=userID).first()
                    print('user email is %s' % user.email)
                    someDict = {'userID': user.id, 'email': user.email, 'company': user.business_name, 'firstName': user.firstName, \
                                'title': user.title, 'bizDesc': user.bizDesc}
                    someList.append(someDict)
                print(someList)
                return jsonify({'response': someList})
            else:
                print('EMPTY')
                return jsonify({'error': 'EMPTY'})
        except Exception:
            print('ERROR')
            return jsonify({'error': 'TROUBLE'})

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = MultiDict(mapping=request.json)
        form = LoginForm(data)

        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                print("user has been found and password has been validated")
                login_user(user, False)
                userDict = {'email':current_user.email, 'name':current_user.firstName, \
                    'title': current_user.title, 'company': current_user.business_name, 'zipcode': current_user.zipAddress, \
                    'employeeNumber': current_user.employeeNumber, 'bizDesc': current_user.bizDesc}
                print("RETURNING")
                return jsonify({'response': userDict})
            else:
                print("Invalid login")
                return jsonify({'error': 'No User'})
        else:
            print("Login does not meet requirements")
            return jsonify({'error': 'Login does not meet requirements'})

    except Exception:
        print("Unable to access login")
        return jsonify({'error': 'Unable to access login'})