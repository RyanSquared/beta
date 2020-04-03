from datetime import datetime, timedelta

from flask import abort, g, safe_join, request

from ..app_view import AppRouteView, response
from ..auth import login_required
from ..models import Asset, db


class ListDevices(AppRouteView):
    # Allows for GET
    # Identifiers: device
    decorators = [login_required]
    template_name = "content_manager/list_devices.html"

    def populate(self):
        device_list = []
        query = request.args.get("search")

        for device in g.user.allowed_devices:
            if query is not None:
                if query.lower() not in device.nickname.lower():
                    continue
            # Calculate human-readable offline time for device
            now = datetime.now()
            offline_delta = now - device.last_ping
            if offline_delta.days > 30:  # x months
                offline_for = str(int(offline_delta.days / 30)) + " months"
            elif offline_delta.days > 0:  # x days
                offline_for = str(int(offline_delta.days)) + " days"
            elif offline_delta.seconds > (60 * 60):  # x hours
                offline_for = str(int(offline_delta.seconds / (60 * 60))) + " hours"
            else:  # x minutes
                offline_for = str(int(offline_delta.seconds / 60)) + " minutes"

            # Add device to list
            device_list.append({
                "device_id": device.device_id,
                "last_ping": device.last_ping.timestamp(),
                "nickname": device.nickname,
                "system_version": device.system_version,
                "device_ip": device.device_ip,
                "total_disk": device.total_disk,
                "free_disk": device.free_disk,
                "offline_for": offline_for,
                "is_offline": offline_delta.days > 0 or offline_delta.seconds > 300,
            })

        return {
            "devices": device_list,
            "current_time": datetime.now(),
            "query": query,
        }
