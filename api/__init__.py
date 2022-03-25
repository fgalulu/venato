import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    from api.admin.routes import admin
    from api.project_manager.routes import project_manager
    from api.developer.routes import developer
    from api.submitter.routes import submitter
    app.register_blueprint(admin)
    app.register_blueprint(project_manager)
    app.register_blueprint(developer)
    app.register_blueprint(submitter)

    return app


from api import models
