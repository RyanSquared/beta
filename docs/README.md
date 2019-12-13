All API routes can use both JSON and HTTP Form attributes to request data, but
output will only be sent to clients that are using JSON, as HTTP form
attributes are intended to be loaded when the page is redirected.

To send data as JSON, make sure the Accept header is set to accept either
`application/json` or `application/*+json`. `application/json` is preferred as
mediaPanel does not define any extensions to the JSON format.

Examples will be formatted in such a way that `>` represents data sent to the
server, and `<` represents data received from the server. The examples will
be copied from `curl` requests which will also be included.

Examples make use of the cURL command line interface `curl`, with the following
aliases for convenience:

```sh
export COOKIEJAR="$HOME/.config/curl/cookiejar"
mkdir -p "$HOME/.config/curl"
alias curl="curl --cookie $COOKIEJAR --cookie-jar $COOKIEJAR"
alias jurl="curl --cookie $COOKIEJAR --cookie-jar $COOKIEJAR -H 'Content-Type: application/json'"
```

To use the Authorization header with the Python `requests` library, the method
should be called like:

```py
import requests

API_URL = "https://beta.getmediapanel.com"
AUTH = ("your_email", "your_password")

response = requests.get(f"{API_URL}/content/device/00f6c1ee/resources",
			auth=AUTH)
```

Additionally, you can use sessions to persist authorization:

```py
import requests

API_URL = "https://beta.getmediapanel.com"
session = requests.Session()

session.auth = ("your_email", "your_password")
response = session.get(f"{API_URL}/content/device/00f6c1ee/resources")
```

You can also use sessions to store cookies, which isn't necessary, but can
avoid sending the same Authorization information for every request:

```py
import requests
API_URL = "https://beta.getmediapanel.com"
session = requests.Session()

session.post(f"{API_URL}/auth/login", json={"email": "your_email",
					    "password": "your_password"})
response = session.get(f"{API_URL}/content/device/00f6c1ee/resources")
```

Remember that if you want to log in as a different user, you should create a
new session or access the `/auth/logout` route to clear the current session's
cookie; even if you're not specifically using cookie-based authentication, the
cookie may be set anyways.

# Routes

## Authentication and Account Management

- [`/auth/register`](routes/auth#register)
- [`/auth/login`](routes/auth#login)

## Content Management

- [`/content/<type>/<target_id>/resources`](routes/content#list-resources)
- [`/content/<type>/<target_id>/resources/new`](routes/content#upload-resource)
- [`/content/<type>/<target_id>/resources/manage/<resource_id>`](routes/content#manage-resource)
- [`/content/<type>/<client_id>/file/<target_id>/<path:filename>`](routes/content#resource-file)
