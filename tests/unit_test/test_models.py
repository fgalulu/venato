from api import bcrypt
from api.models import User, Project, Ticket, Role, UserTicketManagement, UserProjectManagement


def test_user(client):
    """
    test creating new user.
    """
    pwd = bcrypt.generate_password_hash('password').decode('utf-')
    user = User(first_name='Jane', last_name='Doe', email='jane@example.com', password=pwd, role=Role.SUBMITTER)

    assert user
    assert user.get_role() == 'submitter'
    assert user.get_name() == 'Jane Doe'
    assert user.get_email() == 'jane@example.com'
    assert user.check_password('password')
    assert user.get_token()


def test_project(client, new_pm):
    """
    testing creating new project.
    """
    project = Project(name='Project one', description='some description', supervised_by=new_pm.id,
                      created_by=new_pm.id)
    assert project
    assert project.get_name() == "Project one"


def test_ticket(client, new_project, new_pm):
    """
    testing creating new ticket.
    """
    ticket = Ticket(label='Ticket one', description='some description', status='open', created_by=new_pm.id,
                    project=new_project)
    assert ticket
    assert ticket.get_project() == new_project.get_name()
    # assert ticket.get_author() == new_pm.email()


def test_user_project(client, new_project, new_user):
    """
    testing creating new user project relationship
    """
    user_project = UserProjectManagement(user_id=new_user.id, project_id=new_project.id)

    assert user_project
    assert new_project.user_assigned
    assert new_user.project


def test_user_ticket(client, new_ticket, new_user):
    """
    testing creating new user ticket relationship
    """
    user_ticket = UserTicketManagement(user_id=new_user.id, ticket_id=new_ticket.id)

    assert user_ticket
    assert new_ticket.user_assigned
    assert new_user.ticket
