from flask import Blueprint, jsonify, request
from flask.views import MethodView
from api import db
from api.models import Project, Ticket, User, UserProjectManagement, UserTicketManagement
from api.schema import TicketSchema, ProjectSchema, UserSchema
from api.auth import multi_auth


developer = Blueprint('developer', __name__, url_prefix='/developer')


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    developer.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    developer.add_url_rule(url, view_func=view_func, methods=['POST', ])
    developer.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class TicketApi(MethodView):
    """api endpoint for tickets '/tickets/...' """

    decorators = [multi_auth.login_required(role='developer')]

    def get(self, ticket_id):
        if ticket_id:
            schema = TicketSchema(many=False)
            ticket = Ticket.query.get_or_404(ticket_id)
            print(ticket.get_project())
            return jsonify(schema.dump(ticket)), 200
        else:
            # return all tickets
            schema = TicketSchema(many=True)
            qry = UserTicketManagement()
            tickets_assigned = Ticket.query.filter(UserTicketManagement).all()
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


register_api(TicketApi, 'ticket_api', '/tickets/', pk='ticket_id')

#
# @developer.route('/tickets')
# @multi_auth.login_required
# def tickets():
#     schema = TicketSchema(many=True)
#     tickets = Ticket.query.all()
#     return jsonify(schema.dump(tickets)), 200


@developer.route('/tickets/<int:ticket_id>')
@multi_auth.login_required
def ticket(ticket_id):
    schema = TicketSchema(many=False)
    ticket = Ticket.query.get_or_404(ticket_id)
    print(ticket.get_project())
    return jsonify(schema.dump(ticket)), 200


@developer.route('/users/<int:user_id>')
@multi_auth.login_required
def user(user_id):
    schema = UserSchema()
    user = User.query.get_or_404(user_id)
    return jsonify(schema.dump(user)), 200


@developer.route('/projects')
@multi_auth.login_required
def projects():
    schema = ProjectSchema(many=True)
    projects = Project.query.all()
    return jsonify(schema.dump(projects)), 200


@developer.route('/projects/<int:project_id>')
@multi_auth.login_required
def project(project_id):
    schema = ProjectSchema()
    project = Project.query.get_or_404(project_id)
    return jsonify(schema.dump(project)), 200