import os
from datetime import datetime, timedelta

from flask import Flask, g, request, redirect, render_template, jsonify
from werkzeug.contrib.fixers import ProxyFix

import gigaspoon as gs
from mediapanel.config import EventsConfig


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
    from . import auth, models, content_manager
    for item in [auth, models, content_manager]:
        if getattr(item, "init_app", None) is not None:
            item.init_app(app)
        if getattr(item, "blueprint", None) is not None:
            app.register_blueprint(item.blueprint)

    if app.config["SQLALCHEMY_DATABASE_URI"][-8:] == ":memory:":
        with app.app_context():
            models.db.create_all()

    if (app.config["ENV"] == "production" and
            app.config.get("PROXY_MODE") is None):
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
        """
        mediaPanel dashboard index page.

        HTML version contains a device status (online/offline/out of date), an
        expiring/upcoming ads overview, an upcoming calendar and events
        overview, and a storage space overview.
        """

        decorators = [auth.login_redirect]
        template_name = "index.html"

        def populate(self):
            now = datetime.now()
            data = {
                "current_time": int(now.timestamp()),
                "current_version": "60708",  # ::TODO:: get from VERSION.json?
            }

            # Get device information {{{
            devices = []
            online = []
            offline = []
            out_of_date = []
            for device in g.user.allowed_devices:
                last_ping = device.last_ping.timestamp()
                storage_percentage = 1 - device.free_disk / device.total_disk
                offline_delta = data["current_time"] - last_ping
                if offline_delta > (60 * 60 * 24 * 30):  # x months
                    offline_for = str(int(offline_delta / (60 * 60 * 24 * 30))) + " months"
                elif offline_delta > (60 * 60 * 24):  # x days
                    offline_for = str(int(offline_delta / (60 * 60 * 24))) + " days"
                elif offline_delta > (60 * 60):  # x hours
                    offline_for = str(int(offline_delta / (60 * 60))) + " hours"
                else:  # x minutes
                    offline_for = str(int(offline_delta / 60)) + " minutes"

                version_numbers = device.system_version.split(".")
                version = (version_numbers[0] +
                           version_numbers[1].rjust(2, "0") +
                           version_numbers[2].rjust(2, "0"))

                device_json = {
                    "device_id": device.device_id,
                    "nickname": device.nickname,
                    "system_version": version,
                    "offline_for": offline_for,
                    "last_ping": last_ping,
                    "storage_percentage": storage_percentage * 100,
                }
                devices.append(device_json)

                # Sorting online vs offline
                if offline_delta < 90:
                    online.append(device_json)
                else:
                    offline.append(device_json)

                # List of out of date devices
                if version < data["current_version"]:
                    out_of_date.append(device_json)

            data["devices"] = devices
            data["online"] = online
            data["offline"] = offline
            data["out_of_date"] = out_of_date
            # }}}

            # Get ads information {{{
            data["ads"] = {
                "expiring": [],
                "upcoming": [],
            }
            # }}}

            # Get upcoming calendar and events {{{
            upcoming_events = []
            upcoming_range = timedelta(days=30)
            for device in devices:
                event_config = EventsConfig.from_v6_id(
                    g.client.client_id, device["device_id"],
                    base_path=app.config["RESOURCES_FOLDER"])
                for event_name, event in event_config.events.items():
                    for person, date in event.events:
                        event_range = date.replace(year=now.year) - now.date()
                        print(event_range, upcoming_range)
                        if timedelta(0) < event_range < upcoming_range:
                            upcoming_events.append((event_name, person.name,
                                                    date.strftime("%B %d")))
            data["upcoming_events"] = upcoming_events
            # }}}

            return data

    app.add_url_rule("/", view_func=Index.as_view("index"))

    return app
