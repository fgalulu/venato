from flask import Blueprint, jsonify, request
from api import db, bcrypt
from api.auth import verify_password
from api.models import User
from api.errors import error_response

main = Blueprint('main', __name__)


@main.route('/authenticate', methods=['POST'])
def login():
    data = request.get_json()
    if data is None:
        return jsonify('No email or password provided.'), 400
    user = verify_password(data['email'], data['password'])
    if user is None:
        return error_response(400)
    token = user.get_token()
    db.session.commit()
    return jsonify({'message': 'success', 'token': token}), 200


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    pwd = data['password']
    first_name= data['first_name']
    last_name = data['last_name']
    email = data['email']
    user_exist = User.query.filter_by(email=email).first()
    if user_exist:
        return jsonify({'message': 'User with the email address already exists', 'status_code': 400})
    elif first_name != '' or last_name != '' or pwd != '' or email!='':
        hashed_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
        user = User(first_name=first_name, last_name=data['last_name'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'success', 'status_code': 201})
        
    else:
        return jsonify({'message': 'Error, something happened'}), 400