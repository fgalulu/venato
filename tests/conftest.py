from flask import appcontext_popped
import pytest
from api import create_app, db

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

