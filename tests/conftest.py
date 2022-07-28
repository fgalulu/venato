from flask import appcontext_popped
import pytest
from api import create_app, db, bcrypt
from api.models import User, Role, Project


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
    user = User(first_name='first', last_name='last', email='one@example.com', password=pwd)
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
def new_project(client, new_pm, new_admin):
    project = Project(name='project 1', description='some description', supervisor=new_pm,
                      project_author=new_admin)
    db.session.add(project)
    db.session.commit()
    yield project
