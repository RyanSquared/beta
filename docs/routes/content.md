# URL arguments for all following rules

- `type`: Must be one of `device` or `group`
- `target_id`: Either a device ID or a group ID depending on `type`

# Returned values for all following rules

- `type`: Mirrored value of above argument
- `target_id`: Mirrored value of above argument


# Resources

## List Resources

**Route:** `/content/<type>/<target_id>/resources`

**Methods:** `GET`

**Returns:**

- resources[]: Array containing the following fields:
  - id: Unique identifier, for [manage-resource](#manage-resource)
  - filename: Filename used for [resource-file](#resource-file)
  - is_digital_frame: Toggle for whether the resource should be active in the
    Digital Frame app
  - is_display_ad: Toggle for whether the resource should be active and usable
    in the Display Ad app
  - is_alerts: Toggle for whether the resource should be active and usable in
    the Alerts app
  - is_jukebox: Toggle for whether the resource should be active in the
    Jukebox app
  - display_name: Display name used before encoding and stripping spaces
  - thumbnail_name: Filename of thumbnail generated for asset
  - timestamp: UNIX timestamp of when the resource was last updated
  - size: Approximate size in MB of file

## Upload Resource

**Route:** `/content/<type>/<target_id>/resources/new`

**Methods:** `POST`

**Arguments:**

This method takes file uploads

**Returns:**

- upload_ids[]: Identifiers for tracking when the resources will be ready for
  use, intended for [resource-convert-status](#resource-convert-status)

## Resource Convert Status

**TODO** make this a route to poll for mediaConvertQueue

## Manage Resource

**Route:** `/content/<type>/<target_id>/resources/manage/<resource_id>`

**Methods:** `GET`, `PUT`, `DELETE`

**Arguments:**

When the `PUT` method is used, these arguments are expected to update the
resource.

- is_digital_frame: Toggle for whether the resource should be active in the
  Digital Frame app
- is_display_ad: Toggle for whether the resource should be active and usable
  in the Display Ad app
- is_alerts: Toggle for whether the resource should be active and usable in
  the Alerts app
- is_jukebox: Toggle for whether the resource should be active in the
  Jukebox app

**Returns:**

When `DELETE` is used, an empty object will be returned instead, as there is
no longer a resource from which data can be obtained.

- id: Unique identifier, for [manage-resource](#manage-resource)
- filename: Filename used for [resource-file](#resource-file)
- is_digital_frame: Toggle for whether the resource should be active in the
  Digital Frame app
- is_display_ad: Toggle for whether the resource should be active and usable
  in the Display Ad app
- is_alerts: Toggle for whether the resource should be active and usable in
  the Alerts app
- is_jukebox: Toggle for whether the resource should be active in the
  Jukebox app
- display_name: Display name used before encoding and stripping spaces
- thumbnail_name: Filename of thumbnail generated for asset
- timestamp: UNIX timestamp of when the resource was last updated
- size: Approximate size in MB of file

## Resource File

**TODO** eventually support Accept-Range, Content-Range, and Range headers

**Route:** `/content/<type>/<client_id>/file/<target_id>/<path:filename>`

**Arguments:**

- `client_id`: ID of the client by whom the resource is owned
- `filename`: Path for the file, can be gotten from `filename` from the
[list-resources](#list-resources) or [manage-resources](#manage-resources)
routes

**Returns:**

The file pointed to by the above arguments (including `type` and `target_id`),
with the Content-Type header set to the MIME type of the file.
