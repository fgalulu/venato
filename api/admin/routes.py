import json
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from api import db, bcrypt
from api.auth import multi_auth
from api.models import Ticket, User, Project
from api.schema import TicketSchema, UserSchema, ProjectSchema
from .utils import generate_random_password

admin = Blueprint('admin', __name__, url_prefix='/admin')


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    admin.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET',])
    admin.add_url_rule(url, view_func=view_func, methods=['POST',])
    admin.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


@admin.route('/tokens')
@multi_auth.login_required
def get_token():
    token = multi_auth.current_user().get_token()
    db.sesssion.commit()
    return jsonify({'token': token})


class UserAPI(MethodView):
    """api endpoint for users '/users/...' """
    
    decorators = [multi_auth.login_required(role='admin')]

    def get(self, user_id):
        if user_id is None:
            # return list of all users
            schema = UserSchema(many=True)
            users = User.query.all()
            return jsonify(schema.dump(users)), 200
        else:
            # return user
            schema = UserSchema()
            user = User.query.get_or_404(user_id)
            return jsonify(schema.dump(user)), 200

    def post(self, user_id):
        # add new user
        data = request.get_json()
        # print(data)
        first_name= data['first_name']
        last_name = data['last_name']
        email = data['email']
        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            return jsonify('User with the email address already exists'), 400
        elif first_name != '' or last_name != '' or email!='':
            pwd = generate_random_password()
            hashed_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
            user = User(first_name=first_name, last_name=data['last_name'], email=data['email'], password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify('success'), 201
            
        else:
            return jsonify('Error, something happened'), 400
    
    def put(self, user_id):
        # update user
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        if data['first_name']:
            user.first_name = data['first_name']
        if data['last_name']:
            user.last_name = data['last_name']
        if data['email']:
            user.email = data['email']
        if data['password']:
            pwd = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password = pwd
        db.session.commit()
        return jsonify('User edited.'), 200
        pass
    
    def delete(self, user_id):
        # delete user
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify('Deleted successfully!'), 200


class ProjectAPI(MethodView):
    """api for projects endpoint '/projects/...' """
    decators =[multi_auth.login_required(role='admin')]

    def get(self, project_id):
        if project_id is None:
            # return all projects
            schema = ProjectSchema(many=True)
            projects = Project.query.all()
            return jsonify(schema.dump(projects)), 200
        else: 
            schema = ProjectSchema()
            project = Project.query.get_or_404(project_id)
            print(project)
            return jsonify(schema.dump(project)), 200

    def post(self):
        # create new project
        pass

    def put(self, project_id):
        # update project
        pass

    def delete(self, project_id):
        # delete project
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return jsonify('Project deleted.'), 200


class TicketApi(MethodView):
    """api endpoint for tickets '/tickets/...' """

    decorators = [multi_auth.login_required(role='admin')]

    def get(self, ticket_id):
        if ticket_id is None:
            # return all tickets
            schema = TicketSchema(many=True)
            tickets = Ticket.query.all()
            return jsonify(schema.dump(tickets)), 200

        else:
            schema = TicketSchema(many=False)
            ticket = Ticket.query.get_or_404(ticket_id)
            print(ticket.get_project())
            return jsonify(schema.dump(ticket)), 200
    
    def post(self):
        # create new ticket
        data = request.get_json()
        data_label = data['label']
        data_description = data['description']
        data_status = data['status']
        data_created_by = multi_auth.current_user().id
        data_project_id = data['project_id']
        # print(created_by)
        ticket_label_exist = Ticket.query.filter_by(label=data_label).first()
        if ticket_label_exist:
            return jsonify('A ticket with the same label exists.'), 400
        else:
            ticket = Ticket(label=data_label, description=data_description, status=data_status, 
                                created_by=data_created_by, project_id=data_project_id)
            db.session.add(ticket)
            db.session.commit()
            return jsonify(f'TIcket with label "{ticket.label}" created.'), 200

    def put(self, ticket_id):
        # update ticket
        pass

    def delete(self, ticket_id):
        # delete ticket
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete()
        db.session.commit()
        return jsonify(f'Ticket with label "{ticket.label}" deleted.'), 200


register_api(UserAPI, 'user_api', '/users/', pk='user_id')
register_api(ProjectAPI, 'project_api', '/projects/', pk='project_id')
register_api(TicketApi, 'ticket_api', '/tickets/', pk='ticket_id')
