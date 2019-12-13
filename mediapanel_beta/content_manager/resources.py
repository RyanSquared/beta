from flask import (abort, current_app, g, safe_join,
                   send_from_directory, url_for)
from flask.views import MethodView

from ..app_view import AppRouteView, response
from ..auth import login_required
from ..models import Asset, db


class ResourceFile(MethodView):
    def get(self, content_type, client_id, target_id, filename):
        resources_folder = current_app.config["RESOURCES_FOLDER"]
        if content_type == "group":  # Group file
            resource_path = safe_join(resources_folder, client_id, target_id,
                                      "uploaded")
        else:  # Device file
            resource_path = safe_join(resources_folder, client_id, "1",
                                      target_id, "uploaded")
        return send_from_directory(resource_path, filename)


class Resource(AppRouteView):
    # Allow for GET, PUT, PATCH, and DELETE
    # Identifiers: manage_resource, upload_resource
    decorators = [login_required]

    def before_request(self, _type, target_id, resource_id):
        assert resource_id is not None, "missing resource ID"
        # Load object into flask.g
        resource = Asset.query.filter_by(client_id=g.user.client_id,
                                         id=resource_id).first()
        if resource is None:
            return abort(404)  # Resource was not found, raise 404
        g.resource = resource

    def populate(self, _type, target_id, resource_id):
        # Returns link to actual resource file
        resource = g.resource
        resource_url = url_for(".resource_file", content_type=_type,
                               client_id=resource.client_id,
                               target_id=target_id,
                               filename=resource.filename)
        return {
            "type": _type,
            "target_id": target_id,
            "id": resource.id,
            "filename": resource.filename,
            "is_digital_frame": resource.is_digital_frame,
            "is_display_ad": resource.is_display_ad,
            "is_alerts": resource.is_alerts,
            "is_jukebox": resource.is_jukebox,
            "display_name": resource.display_name,
            "thumbnail_name": resource.thumbnail_name,
            "timestamp": int(resource.timestamp.timestamp()),
            "size": resource.size,
            "resource_url": resource_url,
        }

    def handle_put(self, data, _type, target_id, resource_id):
        resource = g.resource
        resource.is_digital_frame = data["is_digital_frame"]
        resource.is_display_ad = data["is_display_ad"]
        resource.is_alerts = data["is_alerts"]
        resource.is_jukebox = data["is_jukebox"]
        db.session.commit()

        resource_url = url_for(".resource_file", content_type=_type,
                               client_id=resource.client_id,
                               target_id=target_id,
                               filename=resource.filename)
        return response(message="Resource successfully updated", payload={
            "type": _type,
            "target_id": target_id,
            "id": resource.id,
            "filename": resource.filename,
            "is_digital_frame": resource.is_digital_frame,
            "is_display_ad": resource.is_display_ad,
            "is_alerts": resource.is_alerts,
            "is_jukebox": resource.is_jukebox,
            "display_name": resource.display_name,
            "thumbnail_name": resource.thumbnail_name,
            "timestamp": int(resource.timestamp.timestamp()),
            "size": resource.size,
            "resource_url": resource_url,
        })

    def handle_patch(self, data, _type, target_id, resource_id):
        resource = g.resource
        if data.get("is_digital_frame") is not None:
            resource.is_digital_frame = data["is_digital_frame"]
        if data.get("is_display_ad") is not None:
            resource.is_display_ad = data["is_display_ad"]
        if data.get("is_alerts") is not None:
            resource.is_alerts = data["is_alerts"]
        if data.get("is_jukebox") is not None:
            resource.is_jukebox = data["is_jukebox"]
        db.session.commit()

        resource_url = url_for(".resource_file", content_type=_type,
                               client_id=resource.client_id,
                               target_id=target_id,
                               filename=resource.filename)
        return response(message="Resource successfully updated", payload={
            "type": _type,
            "target_id": target_id,
            "id": resource.id,
            "filename": resource.filename,
            "is_digital_frame": resource.is_digital_frame,
            "is_display_ad": resource.is_display_ad,
            "is_alerts": resource.is_alerts,
            "is_jukebox": resource.is_jukebox,
            "display_name": resource.display_name,
            "thumbnail_name": resource.thumbnail_name,
            "timestamp": int(resource.timestamp.timestamp()),
            "size": resource.size,
            "resource_url": resource_url,
        })

    def handle_delete(self, _type, target_id, resource_id):
        # Delete record, file, and commit deletion to db
        pass


class NewResource(AppRouteView):
    decorators = [login_required]
    pass


class ListResources(AppRouteView):
    # Identifiers: list_resources
    decorators = [login_required]

    def populate(self, _type, target_id):
        if _type == "device":
            resources = Asset.query.filter_by(client_id=g.user.client_id,
                                              group_id=0,
                                              device_id=target_id)
            return {"type": _type, "target_id": target_id, "resources": [{
                "id": resource.id,
                "filename": resource.filename,
                "is_digital_frame": resource.is_digital_frame,
                "is_display_ad": resource.is_display_ad,
                "is_alerts": resource.is_alerts,
                "is_jukebox": resource.is_jukebox,
                "display_name": resource.display_name,
                "thumbnail_name": resource.thumbnail_name,
                "timestamp": int(resource.timestamp.timestamp()),
                "size": resource.size,
                "resource_url": url_for(".resource_file", content_type=_type,
                                        client_id=resource.client_id,
                                        target_id=resource.device_id,
                                        filename=resource.filename),
            } for resource in resources.all()]}
        else:
            resources = Asset.query.filter_by(client_id=g.user.client_id,
                                              group_id=target_id)
            return {"type": _type, "target_id": target_id, "resources": [{
                "id": resource.id,
                "filename": resource.filename,
                "is_digital_frame": resource.is_digital_frame,
                "is_display_ad": resource.is_display_ad,
                "is_alerts": resource.is_alerts,
                "is_jukebox": resource.is_jukebox,
                "display_name": resource.display_name,
                "thumbnail_name": resource.thumbnail_name,
                "timestamp": int(resource.timestamp.timestamp()),
                "size": resource.size,
                "resource_url": url_for(".resource_file", content_type=_type,
                                        client_id=resource.client_id,
                                        target_id=resource.device_id,
                                        filename=resource.filename),
            } for resource in resources.all()]}
        pass
