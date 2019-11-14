import os

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, redirect, render_template, jsonify

import gigaspoon as gs


def create_app(test_config: dict = None) -> Flask:
    app = Flask(__name__)

    # for usage with proxies
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if test_config is not None:
        app.config.from_mapping(test_config)

    app.config.update(((v[6:], os.environ[v]) for v in os.environ
                       if v[:6] == "FLASK_"))

    print([(v[6:], os.environ[v]) for v in os.environ
           if v[:6] == "FLASK_"])

    from .app_view import AppRouteView, response
    from . import auth, models
    for item in [auth, models]:
        if getattr(item, "init_app", None) is not None:
            item.init_app(app)
        if getattr(item, "blueprint", None) is not None:
            app.register_blueprint(item.blueprint)

    if app.config["SQLALCHEMY_DATABASE_URI"][-8:] == ":memory:":
        with app.app_context():
            models.db.create_all()

    if app.config["ENV"] == "production":
        # require HTTPS in production, do not require in development
        @app.before_request
        def redirect_insecure():
            if not request.is_secure:
                return redirect(request.url.replace("http", "https", 1))

    @app.errorhandler(403)
    def not_authorized(e):
        return render_template("errors/_403.html"), 403

    @app.errorhandler(gs.e.FormError)
    def form_error(e):
        status_code = 400
        value = response("Error for form submission (%s)" % e,
                         payload={"type": str(type(e)), "msg": str(e)},
                         status_code=status_code)

        # return a JSON payload for a FormError
        if request.is_json:
            return jsonify(value), status_code

        # redirect to the current page, clears the form and allows refreshing
        return redirect(request.url_rule.rule)

    class Index(AppRouteView):
        template_name = "index.html"

        def populate(self):
            print(models.User.query.all())
            return {}

    app.add_url_rule("/", view_func=Index.as_view("index"))

    return app
