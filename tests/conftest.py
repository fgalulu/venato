from flask import appcontext_popped
import pytest
from api import create_app, db, bcrypt
from api.models import User, Role, Project, Ticket, UserTicketManagement, UserProjectManagement


@pytest.fixture()
def app():
    app = create_app('testing')
    with app.app_context() as app_context:
        app_context.push()
        db.create_all()
    
    yield app

    db.drop_all()
    app_context.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def new_user(client):
    pwd = bcrypt.generate_password_hash('Pass1234!').decode('utf-8')
    user = User(first_name='first', last_name='last', email='one@example.com', password=pwd, role=Role.SUBMITTER)
    db.session.add(user)
    db.session.commit()
    yield user


@pytest.fixture()
def new_admin(client):
    pwd = bcrypt.generate_password_hash('Pass1234!').decode('utf-8')
    admin = User(first_name='first', last_name='last', email='one@example.com', password=pwd, role=Role.ADMIN)
    db.session.add(admin)
    db.session.commit()
    yield admin


@pytest.fixture()
def new_dev(client):
    pwd = bcrypt.generate_password_hash('Pass1234!').decode('utf-8')
    admin = User(first_name='first', last_name='last', email='one@example.com', password=pwd, role=Role.DEVELOPER)
    db.session.add(admin)
    db.session.commit()
    yield admin


@pytest.fixture()
def new_pm(client):
    pwd = bcrypt.generate_password_hash('Pass1234!').decode('utf-8')
    pm = User(first_name='project', last_name='manager', email='two@example.com', password=pwd,
                 role=Role.PROJECT_MANAGER)
    db.session.add(pm)
    db.session.commit()
    yield pm


@pytest.fixture()
def authorised_admin(new_admin):
    token = new_admin.get_token()
    yield token


@pytest.fixture()
def authorised_dev(new_dev):
    token = new_dev.get_token()
    yield token


@pytest.fixture()
def authorised_pm(new_pm):
    token = new_pm.get_token()
    yield token


@pytest.fixture()
def authorised_submitter(new_user):
    token = new_user.get_token()
    yield token


@pytest.fixture()
def new_project(client, new_pm, new_admin):
    project = Project(name='project 1', description='some description', supervisor=new_pm,
                      project_author=new_admin)
    db.session.add(project)
    db.session.commit()
    yield project


@pytest.fixture()
def new_ticket(new_project, new_pm):
    ticket = Ticket(label='ticket one', description='some description about the ticket',
                    ticket_author=new_pm, project=new_project)
    db.session.add(ticket)
    db.session.commit()
    yield ticket


@pytest.fixture()
def new_user_ticket(new_ticket, new_user):
    user_ticket = UserTicketManagement(user_id=new_user.id, ticket_id=new_ticket.id)

    db.session.add(user_ticket)
    db.session.commit()
    yield user_ticket


@pytest.fixture()
def new_dev_ticket(new_ticket, new_dev):
    dev_ticket = UserTicketManagement(user_id=new_dev.id, ticket_id=new_ticket.id)

    db.session.add(dev_ticket)
    db.session.commit()
    yield dev_ticket


@pytest.fixture()
def new_user_project(new_project, new_user):
    user_project = UserProjectManagement(user_id=new_user.id, project_id=new_project.id)

    db.session.add(user_project)
    db.session.commit()
    yield user_project


@pytest.fixture()
def new_dev_project(new_project, new_dev):
    user_project = UserProjectManagement(user_id=new_dev.id, project_id=new_project.id)

    db.session.add(user_project)
    db.session.commit()
    yield user_project
