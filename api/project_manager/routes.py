from flask import Blueprint
from api import schema
from models import User, Ticket, Project, UserProjectManagement

project_manager = Blueprint('project_manger', __name__)

# @project_manager.route('/')