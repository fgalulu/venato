from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from .models import User
from .errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
@token_auth.get_user_roles
def get_user_roles(user):
    return user.get_role()


from flask import jsonify
from api import db
from api import admin
from api.auth import basic_auth



@admin.route('/tokens')
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.sesssion.commit()
    return jsonify({'token': token})

    
