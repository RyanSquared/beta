from flask import (abort, current_app, g, request, safe_join,
                   send_from_directory, session, url_for)

from ..app_view import AppRouteView
from ..auth import login_required
from ..models import Asset


class ResourceFile(AppRouteView):
    def populate(self, content_type, client_id, target_id, filename):
        resources_folder = current_app.config["RESOURCES_FOLDER"]
        if content_type == "group":  # Group file
            resource_path = safe_join(resources_folder, client_id, target_id,
                                      "uploaded")
        else:  # Device file
            resource_path = safe_join(resources_folder, client_id, "1",
                                      target_id, "uploaded")
        print(resource_path, filename)
        return send_from_directory(resource_path, filename)


class Resource(AppRouteView):
    # Allow for GET, POST, PUT, and DELETE
    # Identifiers: manage_resource, upload_resource
    decorators = [login_required]

    def before_request(self, type, target_id, resource_id):
        if request.method == "POST":
            return
        assert resource_id is not None, "missing resource ID"
        # Load object into flask.g
        resource = Asset.query.filter_by(client_id=session["client_id"],
                                         id=resource_id).first()
        if resource is None:
            return abort(404)  # Resource was not found, raise 404
        g.resource = resource

    def populate(self, type, target_id, resource_id):
        # Returns link to actual resource file
        resource = g.resource
        resource_url = url_for(".resource_file", content_type=type,
                               client_id=resource.client_id,
                               target_id=target_id,
                               filename=resource.filename)
        return {"resource_url": resource_url}

    def handle_post():
        pass

    def handle_put():
        pass

    def handle_delete():
        pass


class NewResource(AppRouteView):
    pass


class ListResources(AppRouteView):
    # Identifiers: list_resources

    def populate():
        pass
