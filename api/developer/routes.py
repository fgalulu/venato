from flask import Blueprint, jsonify
from api.models import Project, Ticket, User, UserProjectManagement, UserTicketManagement
from api.schema import TicketSchema, ProjectSchema, UserSchema
from api.auth import token_auth


developer = Blueprint('developer', __name__, url_prefix='/developer')

@developer.route('/tickets')
@token_auth.login_required
def tickets():
    schema = TicketSchema(many=True)
    tickets = Ticket.query.all()
    return jsonify(schema.dump(tickets)), 200


@developer.route('/tickets/<int:ticket_id>')
@token_auth.login_required
def ticket(ticket_id):
    schema = TicketSchema(many=False)
    ticket = Ticket.query.get_or_404(ticket_id)
    print(ticket.get_project())
    return jsonify(schema.dump(ticket)), 200


@developer.route('/users/<int:user_id>')
@token_auth.login_required
def user(user_id):
    schema = UserSchema()
    user = User.query.get_or_404(user_id)
    return jsonify(schema.dump(user)), 200


@developer.route('/projects')
@token_auth.login_required
def projects():
    schema = ProjectSchema(many=True)
    projects = Project.query.all()
    return jsonify(schema.dump(projects)), 200


@developer.route('/projects/<int:project_id>')
@token_auth.login_required
def project(project_id):
    schema = ProjectSchema()
    project = Project.query.get_or_404(project_id)
    return jsonify(schema.dump(project)), 200