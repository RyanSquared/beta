All API routes can use both JSON and HTTP Form attributes to request data, but
output will only be sent to clients that are using JSON, as HTTP form
attributes are intended to be loaded when the page is redirected.

To send data as JSON, make sure the Accept header is set to accept either
`application/json` or `application/*+json`. `application/json` is preferred as
mediaPanel does not define any extensions to the JSON format.

Examples will be formatted in such a way that `>` represents data sent to the
server, and `<` represents data received from the server. The examples will
be copied from `curl` requests which will also be included.

# Routes

## Authentication and Account Management

- [`/auth/register`](routes/auth#register)
- [`/auth/login`](routes/auth#login)

## Content Management

- [`/content/<type>/<target_id>/resources`](routes/content_manager#list-resources)
- [`/content/<type>/<target_id>/resources/new`](routes/content_manager#upload-resource)
- [`/content/<type>/<target_id>/resources/manage/<resource_id>`](routes/content_manager#manage-resource)
- [`/content/<type>/<client_id>/file/<target_id>/<path:filename>`](routes/content_manager#resource-file)
