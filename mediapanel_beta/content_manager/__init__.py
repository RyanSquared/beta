from flask import Blueprint

from .resources import ListResources, NewResource, Resource, ResourceFile
from .device_list import ListDevices

blueprint = Blueprint("content_manager", __name__, url_prefix="/manage")


# Resources
blueprint.add_url_rule("/<_type>/<target_id>/resources",
                       view_func=ListResources.as_view("list_resources"))
blueprint.add_url_rule("/<_type>/<target_id>/resources/new",
                       view_func=NewResource.as_view("upload_resource"))
blueprint.add_url_rule("/<_type>/<target_id>/resources/by-id/<resource_id>",
                       view_func=Resource.as_view("manage_resource"))
blueprint.add_url_rule(
        "/<content_type>/<client_id>/file/<target_id>/<path:filename>",
        view_func=ResourceFile.as_view("resource_file"))

# Device-specific Applications
blueprint.add_url_rule("/device",
                       view_func=ListDevices.as_view("list_devices"))
