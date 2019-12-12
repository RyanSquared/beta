# URL arguments for all following routes

- `type`: Must be one of `device` or `group`
- `target_id`: Either a device ID or a group ID depending on `type`

# Returned values for all following routes

- `type`: Mirrored value of above argument
- `target_id`: Mirrored value of above argument

# Errors for all the following routes (unless otherwise mentioned)

- HTTP 403: The user was not authenticated for the request, and needs to either
  have the Authorization header set following the BASIC Authorization standard,
  or store cookies to ensure the HTTP client remains logged in.

- HTTP 404: The target ID was not found or an asset relating to the given
  target ID was not found.

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
  - resource_url: URL usable to get the raw resource file

**Example:**

```
# curl -v localhost:5000/content/device/00f6c1ee/resources -H "Content-Type: application/json"            
*   Trying ::1:5000...
* TCP_NODELAY set
* Connected to localhost (::1) port 5000 (#0)
> GET /content/device/00f6c1ee/resources HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Accept: */*
> Cookie: session=eyJjbGllbnRfaWQiOjEsInVzZXJfaWQiOjM2M30.XfA73A.ARyLHxHYfam4I0lIseJs22uv1Ls
> Content-Type: application/json
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.15.8
< Date: Wed, 11 Dec 2019 23:16:41 GMT
< Content-Type: application/json
< Content-Length: 1232
< Connection: keep-alive
< Vary: Cookie
< 
{
  "resources": [
    {
      "display_name": "uservideoyoutubemountaindewanimatedlogo221280x720hd720", 
      "filename": "user_video_122350607_uservideoyoutubemountaindewanimatedlogo221280x720hd720.mp4", 
      "id": 6752, 
      "is_alerts": false, 
      "is_digital_frame": true, 
      "is_display_ad": true, 
      "is_jukebox": false, 
      "resource_url": "/content/device/1/file/00f6c1ee/user_video_122350607_uservideoyoutubemountaindewanimatedlogo221280x720hd720.mp4", 
      "size": 1.25, 
      "thumbnail_name": "user_video_thumb_122350607_uservideoyoutubemountaindewanimatedlogo221280x720hd720.png", 
      "timestamp": 1525438927
    }, 
    {
      "display_name": "14303676 VID20180213114312", 
      "filename": "user_video_14303676_vid20180213114312-rotate90.mp4", 
      "id": 6785, 
      "is_alerts": false, 
      "is_digital_frame": false, 
      "is_display_ad": true, 
      "is_jukebox": false, 
      "resource_url": "/content/device/1/file/00f6c1ee/user_video_14303676_vid20180213114312-rotate90.mp4", 
      "size": 4.57, 
      "thumbnail_name": "user_video_thumb_14303676_vid20180213114312-rotate90.png", 
      "timestamp": 1522692211
    }
  ], 
  "target_id": "00f6c1ee", 
  "type": "device"
}
```

---

## Upload Resource

**Route:** `/content/<type>/<target_id>/resources/new`

**Methods:** `POST`

**Arguments:**

This method takes file uploads

**Returns:**

- upload_ids[]: Identifiers for tracking when the resources will be ready for
  use, intended for [resource-convert-status](#resource-convert-status)

---

## Resource Convert Status

**TODO** make this a route to poll for mediaConvertQueue

---

## Manage Resource

**Route:** `/content/<type>/<target_id>/resources/manage/<resource_id>`

**Methods:** `GET`, `PUT`, `PATCH`, `DELETE`

**Arguments:**

When the `PUT` method is used, all arguments are expected to update the
resource. When the `PATCH` method is used, only arguments that are changed can
be provided.

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
- resource_url: URL usable to get the raw resource file

**Example:**

```
# jurl -v localhost:5000/content/device/00f6c1ee/resources/manage/6785
*   Trying ::1:5000...
* TCP_NODELAY set
* Connected to localhost (::1) port 5000 (#0)
> GET /content/device/00f6c1ee/resources/manage/6785 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Accept: */*
> Cookie: session=eyJjbGllbnRfaWQiOjEsInVzZXJfaWQiOjM2M30.XfA73A.ARyLHxHYfam4I0lIseJs22uv1Ls
> Content-Type: application/json
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.15.8
< Date: Wed, 11 Dec 2019 23:13:33 GMT
< Content-Type: application/json
< Content-Length: 518
< Connection: keep-alive
< Vary: Cookie
< 
{
  "display_name": "14303676 VID20180213114312", 
  "filename": "user_video_14303676_vid20180213114312-rotate90.mp4", 
  "id": 6785, 
  "is_alerts": false, 
  "is_digital_frame": false, 
  "is_display_ad": true, 
  "is_jukebox": false, 
  "resource_url": "/content/device/1/file/00f6c1ee/user_video_14303676_vid20180213114312-rotate90.mp4", 
  "size": 4.57, 
  "target_id": "00f6c1ee", 
  "thumbnail_name": "user_video_thumb_14303676_vid20180213114312-rotate90.png", 
  "timestamp": 1522692211, 
  "type": "device"
}
```

```
# jurl -v localhost:5000/content/device/00f6c1ee/resources/manage/6785 -XPUT \
       -d '{"is_alerts": false, "is_digital_frame": false, "is_jukebox": false, "is_display_ad": true}'
*   Trying ::1:5000...
* TCP_NODELAY set
* Connected to localhost (::1) port 5000 (#0)
> PUT /content/device/00f6c1ee/resources/manage/6785 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Accept: */*
> Cookie: session=eyJjbGllbnRfaWQiOjEsInVzZXJfaWQiOjM2M30.XfA73A.ARyLHxHYfam4I0lIseJs22uv1Ls
> Content-Type: application/json
> Content-Length: 91
> 
* upload completely sent off: 91 out of 91 bytes
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.15.8
< Date: Thu, 12 Dec 2019 00:08:35 GMT
< Content-Type: application/json
< Content-Length: 518
< Connection: keep-alive
< Vary: Cookie
< 
{
  "display_name": "14303676 VID20180213114312", 
  "filename": "user_video_14303676_vid20180213114312-rotate90.mp4", 
  "id": 6785, 
  "is_alerts": false, 
  "is_digital_frame": false, 
  "is_display_ad": true, 
  "is_jukebox": false, 
  "resource_url": "/content/device/1/file/00f6c1ee/user_video_14303676_vid20180213114312-rotate90.mp4", 
  "size": 4.57, 
  "target_id": "00f6c1ee", 
  "thumbnail_name": "user_video_thumb_14303676_vid20180213114312-rotate90.png", 
  "timestamp": 1576108784, 
  "type": "device"
}
```

---

## Resource File

This route allows you to use ranges to download partial bodies, which can be
useful if a download has been interrupted.

**Route:** `/content/<type>/<client_id>/file/<target_id>/<path:filename>`

**Arguments:**

- `client_id`: ID of the client by whom the resource is owned
- `filename`: Path for the file, can be gotten from `filename` from the
[list-resources](#list-resources) or [manage-resources](#manage-resources)
routes

**Returns:**

The file pointed to by the above arguments (including `type` and `target_id`),
with the Content-Type header set to the MIME type of the file.

**Errors:**

HTTP 400:

- The client represented by `client_id` does not exist.
- The group or device represented by `target_id` does not exist.
- The file represented by `filename` does not exist.

**Example:**

```
# curl -v localhost:5000/content/device/1/file/00f6c1ee/user_video_14303676_vid20180213114312-rotate90.mp4 
*   Trying ::1:5000...
* TCP_NODELAY set
* Connected to localhost (::1) port 5000 (#0)
> GET /content/device/1/file/00f6c1ee/user_video_14303676_vid20180213114312-rotate90.mp4 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.15.8
< Content-Type: video/mp4
< Content-Length: 4791626
< Connection: keep-alive
< Last-Modified: Wed, 11 Dec 2019 01:20:39 GMT
< Cache-Control: public, max-age=43200
< Expires: Thu, 12 Dec 2019 12:22:22 GMT
< ETag: "1576027239.2953112-4791626-1912543733"
< Date: Thu, 12 Dec 2019 00:22:22 GMT
< Accept-Ranges: bytes
< 
Warning: Binary output can mess up your terminal. Use "--output -" to tell 
Warning: curl to output it to your terminal anyway, or consider "--output 
Warning: <FILE>" to save to a file.
* Failed writing body (0 != 16384)
```
