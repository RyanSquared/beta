import string  # password requirements
import hashlib  # password hash generation and verification
import uuid  # UUID4 generation

import gigaspoon as gs  # form validation

from mediapanel.db.user import UserType

from flask import Blueprint, request, session
from werkzeug.security import gen_salt

from .app_view import AppRouteView, response
from .models import User, Client, db  # proxy for noticast util

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def check_login(password, email: str = None, user: User = None):
    if email is None and user is None:
        raise ValueError("expected `username` or `user`")
    elif email is not None and user is not None:
        raise ValueError("expected `username` or `user`, not both")
    if user is None:
        user = User.query.filter(User.email.like(email)).first()
    if user is not None:
        hash_object = hashlib.sha512(user.salt.encode("utf8"))
        hash_object.update(password.encode("utf8"))
        if hash_object.hexdigest().lower() == user.password.lower():
            return user
    return None


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
        client = Client(email=values["email"], uuid=str(uuid.uuid4()))
        db.session.add(client)
        db.session.commit()

        try:
            # Generate password hash
            pwsalt = gen_salt(10)
            pwhash_object = hashlib.sha512(pwsalt.encode("utf8"))
            pwhash_object.update(values["password"].encode("utf8"))

            # Create user
            user = User(
                client_id=client.client_id,
                type=UserType.client,
                first_name=values["first_name"],
                last_name=values["last_name"],
                email=values["email"],
                password=pwhash_object.hexdigest().upper(),
                salt=pwsalt,
                get_alert_emails=0)
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.delete(client)
            db.session.commit()
        return response("Successfully registered %s" % values["email"],
                        payload={"email": values["email"],
                                 "uuid": user.client.uuid})


class Login(AppRouteView):
    decorators = [
        gs.flask.validator({
            "email": gs.v.Exists(),
            "password": gs.v.Exists(),
        })
    ]
    template_name = "login.html"

    def handle_post(self, values):
        self.redirect_to = "index"
        email = values["email"]

        user = check_login(values["password"], email=email)
        if user is None:
            self.redirect_to = request.url_rule.rule
            return response("Username or password incorrect", 401)

        session.clear()
        session["user_id"] = user.user_id
        session["client_id"] = user.client_id

        return response("Successfully logged in as %s" % email,
                        payload={"email": email, "uuid": user.client.uuid})


blueprint.add_url_rule("/register", view_func=Register.as_view("register"))
blueprint.add_url_rule("/login", view_func=Login.as_view("login"))
