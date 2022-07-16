from .models import Project, User, Ticket, UserProjectManagement, UserTicketManagement
from api import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password", "created_at", "updated_at")

    role = ma.Function(lambda obj: obj.get_role(), dump_only=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        exclude = ("created_at", "updated_at")

    project_author = ma.Nested(UserSchema)
    supervisor = ma.Nested(UserSchema)
    # user_assigned = ma.Nested(UserSchema, exclude=["role"])
    # tickets = ma.Nested(TicketSchema)


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        exclude = ("created_at", "updated_at")
        # include_fk = True

    project = ma.Nested(ProjectSchema)
    ticket_author = ma.Nested(UserSchema)


class UserTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserTicketManagement
        # exclude = ("updated_at")

    user = ma.Nested(UserSchema)
    ticket = ma.Nested(TicketSchema)


class UserProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProjectManagement
        # exclude = ("updated_at")

    user = ma.Nested(UserSchema)
    project = ma.Nested(ProjectSchema)
