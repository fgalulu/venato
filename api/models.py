import email
from api import db, bcrypt
from datetime import datetime, timedelta
import base64
import os

class Role:
    ADMIN = 200
    PROJECT_MANAGER = 201
    DEVELOPER = 202
    SUBMITTER = 203

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55), nullable=False)
    last_name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role = db.Column(db.SmallInteger, nullable=False, default= Role.SUBMITTER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def get_role(self):
        if self.role == Role.ADMIN:
            return 'admin'
        elif self.role == Role.PROJECT_MANAGER:
            return 'project manager'
        elif self.role == Role.DEVELOPER:
            return 'developer'
        elif self.role == Role.SUBMITTER:
            return 'submitter'


    def get_name(self):
        name = self.first_name + ' ' + self.last_name
        return name

    def get_email(self):
        email = self.email
        return email

    # def get_role(self):
    #     return role

    def check_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    supervised_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supervisor = db.relationship('User', backref='supervisor_project', cascade="all,delete", foreign_keys=[supervised_by])
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_author = db.relationship('User', backref='project_author', cascade="all,delete", foreign_keys=[created_by])
    archived = db.Column(db.Boolean)

    def get_name(self):
        name = self.name
        return name


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(250), nullable=False, default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_author = db.relationship('User', backref='ticket_author', cascade="all,delete", foreign_keys=[created_by])
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='project', cascade="all,delete")


    def get_author(self):
        return self.author.get_email()

    def get_project(self):
        return self.project.get_name()


class UserProjectManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user', cascade="all,delete")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='belongs', cascade="all,delete")

    def get_user(self):
        return self.user.get_name()

    def get_project(self):
        return self.project.get_name()


class UserTicketManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='assingee', cascade="all,delete", foreign_keys=[user_id])
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    ticket = db.relationship('Ticket', backref='ticket', cascade="all,delete")
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='assigner', cascade="all,delete", foreign_keys=[created_by])
