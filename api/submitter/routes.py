from flask import Blueprint, jsonify, request
from flask.views import MethodView

from api import db

from api.auth import multi_auth
from api.models import Ticket
from api.schema import TicketSchema


submitter = Blueprint('submitter', __name__)


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    submitter.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    submitter.add_url_rule(url, view_func=view_func, methods=['POST', ])
    submitter.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class TicketApi(MethodView):
    """api endpoint for tickets '/tickets/...' """

    decorators = [multi_auth.login_required(role='developer')]

    def get(self, ticket_id):
        if ticket_id:
            schema = TicketSchema(many=False)
            ticket = Ticket.query.get_or_404(ticket_id)
            # print(ticket.get_project())
            return jsonify(schema.dump(ticket)), 200
        else:
            # return all tickets
            schema = TicketSchema(many=True)
            tickets_assigned = Ticket.query.filter().all()
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


register_api(TicketApi, 'ticket_api', '/tickets/', pk='ticket_id')
