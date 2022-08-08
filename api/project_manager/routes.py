from flask import Blueprint, jsonify, request
from flask.views import MethodView
from api.models import User, Ticket, Project, UserProjectManagement, UserTicketManagement, Role
from api.schema import TicketSchema, UserSchema, ProjectSchema, UserTicketSchema, UserProjectSchema
from api.auth import multi_auth
from api.errors import error_response

from api import db

project_manager = Blueprint('pm', __name__, url_prefix='/pm')


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    project_manager.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    project_manager.add_url_rule(url, view_func=view_func, methods=['POST', ])
    project_manager.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class TicketApi(MethodView):
    """api endpoint for tickets '/tickets/...' """

    decorators = [multi_auth.login_required(role='pm')]

    def get(self, ticket_id):
        if ticket_id:
            schema = TicketSchema(many=False)
            ticket = Ticket.query.get_or_404(ticket_id)
            # print(ticket.get_project())
            return jsonify(schema.dump(ticket)), 200
        else:
            # return all tickets
            schema = TicketSchema(many=True)
            qry = UserTicketManagement.query.filter_by(user_id=multi_auth.current_user().id).exists()
            tickets_assigned = Ticket.query.filter(qry).all()
            return jsonify(schema.dump(tickets_assigned)), 200

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


class UserAPI(MethodView):
    """ api endpoint for users  /users/"""

    decorators = [multi_auth.login_required(role='pm')]

    def get(self, user_id):
        if user_id:
            schema = UserSchema(many=False)
            user = User.query.get_or_404(user_id)
            return jsonify(schema.dump(user)), 200
        else:
            # return all tickets
            schema = TicketSchema(many=True)
            users = User.query.filter_by(role=Role.DEVELOPER).all()
            return jsonify(schema.dump(users)), 200


class ProjectAPI(MethodView):
    """ api endpoint for projects  /projects/"""

    decorators = [multi_auth.login_required(role='pm')]

    def get(self, project_id):
        if project_id:
            schema = ProjectSchema()
            project = Project.query.filter(Project.supervised_by == multi_auth.current_user().id, Project.id == project_id).first()
            if project:
                return jsonify(schema.dump(project)), 200
            else:
                return error_response(404)
        else:
            schema = ProjectSchema(many=True)
            projects = Project.query.filter_by(supervisor=multi_auth.current_user()).all()
            return jsonify(schema.dump(projects)), 200

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
            return jsonify('success'), 201
        else:
            return jsonify("Supervisor doesnt exist."), 404

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
            return jsonify('success'), 200
        return jsonify("Supervisor doesnt exist."), 404

    def delete(self, project_id):
        # delete project
        project = Project.query.get_or_404(project_id)
        print(project)
        db.session.delete(project)
        db.session.commit()
        return jsonify('Project deleted.'), 200


class UserTicketAPI(MethodView):
    """ api endpoint for user ticket assignment """

    decorators = [multi_auth.login_required(role='pm')]

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
        ticket = Ticket.query.get_or_404(data['ticket_id'])
        user = User.query.get_or_404(data['user_id'])
        user_ticket = UserTicketManagement(user_id=user.id, ticket_id=ticket.id)
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
    """ api endpoint for user ticket assignment """

    decorators = [multi_auth.login_required(role='pm')]

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
        user_project = UserProjectManagement(user_id=user.id, project_id=project.id)
        db.session.add(user_project)
        db.session.commit()
        return jsonify('success'), 200

    def put(self, user_project_id):
        data = request.get_json()
        user_project = UserProjectManagement.query.get_or_404(user_project_id)
        user = User.query.get_or_404(data['user_id'])
        project = Project.query.get_or_404(data['project_id'])
        user_project.user_id = user.id
        user_project.project_id = project.id
        db.session.commit()
        return jsonify('success'), 200

    def delete(self, user_project_id):
        user_project = UserProjectManagement.query.get_or_404(user_project_id)
        db.session.delete(user_project)
        db.session.commit()
        return jsonify('success'), 200


register_api(TicketApi, 'ticket_api', '/tickets/', pk='ticket_id')
register_api(UserAPI, 'user_api', '/users/', pk='user_id')
register_api(ProjectAPI, 'project_api', '/projects/', pk='project_id')
register_api(UserTicketAPI, 'user_ticket_api', '/user-tickets/', pk='user_ticket_id')
register_api(UserProjectAPI, 'user-project_api', '/user-projects/', pk='user_project_id')


@project_manager.get('/projects/<int:project_id>/users')
@multi_auth.login_required(role='pm')
def project_assignee(project_id):
    project = Project.query.get_or_404(project_id)
    users = User.query.join(UserProjectManagement).filter(UserProjectManagement.project_id == project.id).all()
    schema = UserSchema(many=True)
    return jsonify({'project_id': project.id, 'members': schema.dump(users)})
