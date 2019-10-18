import functools  # decorator
import string  # password requirements

import gigaspoon as gs  # form validation

from mediapanel.db.user import UserType

from flask import Blueprint
from werkzeug import check_password_hash, generate_password_hash
# usage: format string like sha256:<salt goes here>:<hash goes here>
# ::TODO:: reformat database to have user-accessible hashes
# ::TODO:: how to store hash and salt in a way that makes ColdFusion and
#          werkzeug both happy
#          \- format string to sha256$salt$hash or whatever for werkzeug

from .app_view import AppRouteView
from .models import IntegrityError, User, Client, db  # proxy for noticast util

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class PassCharRequirement(gs.v.Validator):
    name = "pass_char"

    def validate(self, form, key, value):
        # check if we have one uppercase, one lowercase
        if not set(value) & set(string.ascii_uppercase):
            self.raise_error(key, "*" * len(value),
                             message="missing an uppercase character")
        if not set(value) & set(string.ascii_lowercase):
            self.raise_error(key, "*" * len(value),
                             message="missing a lowercase character")


class UniqueEmailRequirement(gs.v.Validator):
    name = "unique_email"

    def validate(self, form, key, value):
        # check if this client doesn't already exist
        if Client.query.filter_by(email=value).first() is not None:
            self.raise_error(key, value,
                             message="Client already exists with this email")


class Register(AppRouteView):
    decorators = [
        gs.flask.validator({
            "email": [gs.v.Email(), UniqueEmailRequirement()],
            "password": [gs.v.Length(min=6, max=64),
                         PassCharRequirement()],
            "first_name": gs.v.Exists(),
            "last_name": gs.v.Exists(),
        })
    ]
    template_name = "reg.html"

    def handle_post(self, values):
        # Create client
        client = Client(email=values["email"])
        db.session.add(client)
        db.session.commit()

        # Generate password hash
        _, pwsalt, pwhash = generate_password_hash(
                values["password"],
                method="sha512").split("$")

        # Create user
        user = User(
            client_id=client.client_id,
            type=UserType.client,
            first_name=values["first_name"],
            last_name=values["last_name"],
            email=values["email"],
            password=pwhash,
            salt=pwsalt,
            get_alert_emails=0)
        db.session.add(user)
        db.session.commit()
        return {}


blueprint.add_url_rule("/register", view_func=Register.as_view("register"))
