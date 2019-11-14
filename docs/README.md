All API routes can use both JSON and HTTP Form attributes to request data, but
output will only be sent to clients that are using JSON, as HTTP form
attributes are intended to be refreshed when the page is redirected.

To send data as JSON, make sure the Accept header is set to accept either
`application/json` or `application/*+json`. `application/json` is preferred as
mediaPanel does not define any extensions to the JSON format.

Examples will be formatted in such a way that `>` represents data sent to the
server, and `<` represents data received from the server. The examples will
be copied from `curl` requests which will also be included.

# Routes

- [`/auth/register`](routes/auth#register)
- [`/auth/login`](routes/auth#login)
