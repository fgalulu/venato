from .models import Project, User, Ticket
from api import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password", "created_at", "updated_at")


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        exclude = ("created_at", "updated_at")

    author_name = ma.Function(lambda obj: obj.author.get_name(), dump_only=True)
    supervisor_name = ma.Function(lambda obj: obj.supervisor.get_name(), dump_only=True)



class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        exclude = ("created_at", "updated_at")
        # include_fk = True

    project_name = ma.Function(lambda obj: obj.project.get_name(), dump_only=True)
    author_name = ma.Function(lambda obj: obj.author.get_name(), dump_only=True)
