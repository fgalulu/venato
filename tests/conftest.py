from flask import appcontext_popped
import pytest
from api import create_app, db, bcrypt
from api.models import User, Role


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
def authorised_admin(new_admin):
    token = new_admin.get_token()
    yield token
