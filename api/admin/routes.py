import json
from flask import Blueprint, jsonify, request
from api import db, bcrypt
from api.auth import token_auth, verify_password
from api.errors import error_response
from api.models import Ticket, User, Project
from api.schema import TicketSchema, UserSchema, ProjectSchema

admin = Blueprint('admin', __name__)


@admin.route('/authenticate', methods=['POST'])
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


@admin.route('/register', methods=['POST'])
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


@admin.route('/tickets')
@token_auth.login_required
def tickets():
    schema = TicketSchema(many=True)
    tickets = Ticket.query.all()
    return jsonify(schema.dump(tickets)), 200


@admin.route('/tickets/<int:ticket_id>')
@token_auth.login_required
def ticket(ticket_id):
    schema = TicketSchema(many=False)
    ticket = Ticket.query.get_or_404(ticket_id)
    print(ticket.get_project())
    return jsonify(schema.dump(ticket)), 200


@admin.route('/users')
@token_auth.login_required
def users():
    schema = UserSchema(many=True)
    users = User.query.all()
    return jsonify(schema.dump(users)), 200



@admin.route('/users/<int:user_id>')
@token_auth.login_required
def user(user_id):
    schema = UserSchema()
    user = User.query.get_or_404(user_id)
    return jsonify(schema.dump(user)), 200


@admin.route('/projects')
@token_auth.login_required
def projects():
    schema = ProjectSchema(many=True)
    projects = Project.query.all()
    return jsonify(schema.dump(projects)), 200


@admin.route('/projects/<int:project_id>')
@token_auth.login_required
def project(project_id):
    schema = ProjectSchema()
    project = Project.query.get_or_404(project_id)
    return jsonify(schema.dump(project)), 200