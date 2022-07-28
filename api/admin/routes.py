import json
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from api import db, bcrypt
from api.auth import multi_auth, token_auth, basic_auth
from api.models import Ticket, User, Project, UserTicketManagement, UserProjectManagement
from api.schema import TicketSchema, UserSchema, ProjectSchema, UserTicketSchema, UserProjectSchema
from .utils import generate_random_password

admin = Blueprint('admin', __name__, url_prefix='/admin')


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    admin.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    admin.add_url_rule(url, view_func=view_func, methods=['POST', ])
    admin.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


@admin.route('/token')
@multi_auth.login_required
def get_token():
    token = multi_auth.current_user().get_token()
    db.session.commit()
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

    def post(self):
        # add new user
        data = request.get_json()
        print(data)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            return jsonify('User with the email address already exists'), 400
        elif first_name != '' or last_name != '' or email != '':
            pwd = generate_random_password()
            hashed_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
            user = User(first_name=first_name, last_name=data['last_name'], email=data['email'],
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'success', 'password': pwd}), 201

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
    decorators = [multi_auth.login_required(role='admin')]

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
        data = request.get_json()
        # print(multi_auth.current_user())
        # print(token_auth.current_user())
        # print(basic_auth.current_user())
        supervisor = User.query.filter(User.role == 201).filter_by(id=data['supervisor']).first()
        if supervisor:
            project = Project(name=data['name'], description=data['desc'], project_author=multi_auth.current_user(),
                              supervisor=supervisor, archived=False)
            db.session.add(project)
            db.session.commit()
            return jsonify('success'), 200
        else:
            return jsonify("Operation not allowed"), 404

    def put(self, project_id):
        # update project
        data = request.get_json()
        project = Project.query.get_or_404(project_id)
        supervisor = User.query.filter(User.role == 201).filter_by(id=data['supervisor']).first()
        if supervisor:
            project.name = data['name']
            project.description = data['desc']
            project.supervisor = supervisor
            db.session.commit()
            return jsonify('sucecss'), 200
        else:
            return jsonify("Operation not allowed"), 404

    def delete(self, project_id):
        # delete project
        project = Project.query.get_or_404(project_id)
        print(project)
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
        data_description = data['desc']
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
            return jsonify(f'Ticket with label {ticket.label} created.'), 200

    def put(self, ticket_id):
        # update ticket
        data = request.get_json()
        ticket = Ticket.query.get_or_404(ticket_id)
        ticket.label = data['label']
        ticket.description = data['desc']
        ticket.status = data['status']
        ticket.project_id = data['project_id']
        db.session.commit()
        return jsonify('success'), 200

    def delete(self, ticket_id):
        # delete ticket
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        return jsonify(f'Ticket with label {ticket.label} deleted.'), 200


class UserTicketAPI(MethodView):
    decorators = [multi_auth.login_required(role='admin')]

    def get(self, user_ticket_id):
        if user_ticket_id:
            # return one user ticket relationship
            user_ticket = UserTicketManagement.query.get_or_404(user_ticket_id)
            schema = UserTicketSchema()
            return jsonify(schema.dump(user_ticket))
        else:
            # return all user ticket relationships
            user_tickets = UserTicketManagement.query.all()
            schema = UserTicketSchema(many=True)
            return jsonify(schema.dump(user_tickets)), 200

    def post(self):
        data = request.get_json()
        user_ticket = UserTicketManagement(user_id=data['user_id'], ticket_id=data['ticket_id'],
                                           author=multi_auth.current_user())
        db.session.add(user_ticket)
        db.session.commit()
        return jsonify('success'), 200

    def put(self, user_ticket_id):
        data = request.get_json()
        user_ticket = UserTicketManagement.query.get_or_404(user_ticket_id)
        user = User.query.get_or_404(data['user_id'])
        ticket = Ticket.query.get_or_404(data['ticket_id'])
        user_ticket.user_id = user.id
        user_ticket.ticket_id = ticket.id
        db.session.commit()
        return jsonify('success'), 200

    def delete(self, user_ticket_id):
        user_ticket = UserTicketManagement.query.get_or_404(user_ticket_id)
        db.session.delete(user_ticket)
        db.session.commit()
        return jsonify('success'), 200


class UserProjectAPI(MethodView):

    decorators = [multi_auth.login_required(role='admin')]

    def get(self, user_project_id):
        if user_project_id:
            user_project = UserProjectManagement.query.get_or_404(user_project_id)
            schema = UserProjectSchema()
            return jsonify(schema.dump(user_project))
        else:
            user_projects = UserProjectManagement.query.all()
            schema = UserProjectSchema(many=True)
            return jsonify(schema.dump(user_projects))

    def post(self):
        data = request.get_json()
        user = User.query.get_or_404(data['user_id'])
        project = Project.query.get_or_404(data['project_id'])
        user_project = UserProjectManagement(user=user, project=project)
        db.session.add(user_project)
        db.session.commit()
        return jsonify('success'), 200

    def put(self, user_project_id):
        data = request.get_json()
        user_project = UserProjectManagement.query.get_or_404(user_project_id)
        user_project.user_id = data['user_id']
        user_project.project_id = data['project_id']
        db.session.commit()
        return jsonify('success'), 200

    def delete(self, user_project_id):
        user_project = UserProjectManagement.query.get_or_404(user_project_id)
        db.session.delete(user_project)
        db.session.commit()
        return jsonify('success'), 200


register_api(UserAPI, 'user_api', '/users/', pk='user_id')
register_api(ProjectAPI, 'project_api', '/projects/', pk='project_id')
register_api(TicketApi, 'ticket_api', '/tickets/', pk='ticket_id')
register_api(UserTicketAPI, 'user_ticket_api', '/user-tickets/', pk='user_ticket_id')
register_api(UserProjectAPI, 'user-project_api', '/user-projects/', pk='user_project_id')


@admin.get('/project/<int:project_id>/users')
@multi_auth.login_required(role='admin')
def project_assigned(project_id):
    project = Project.query.get_or_404(project_id)
    users = User.query.join(UserProjectManagement).filter(UserProjectManagement.project_id == project.id).all()
    schema = UserSchema(many=True)
    return jsonify({'project_id': project.id, 'members': schema.dump(users)})
