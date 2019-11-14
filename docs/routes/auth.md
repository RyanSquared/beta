# Register

**Route:** `/auth/register`

**Arguments:**

- email (example: ryan@getmediapanel.com)
- password (example: Password01)
  - Must contain: one capital letter, one lowercase letter
  - Must be at least 6 characters, at most 64
- first_name
- last_name

**Returns:**

- email: Email used to log in
- uuid: UUID4 used to identify the client

**Errors:**

HTTP 400:

- UniqueEmailRequrement: Email was already used with a previous client.
- PassCharRequirement: Password does not match character requirements.
- Length: Password does not meet length requirements.

**Example:**

```
# curl -v -XPOST https://beta.mediapanel.fusionscript.info/auth/register \
 -d'{"email": "1ryan@educatethewait.com", "password": "Password01", ' \
    '"first_name": "Ryan", "last_name": "Heywood"}' \
 -H "Content-Type: application/json"

POST /auth/register HTTP/1.1
> Host: beta.mediapanel.fusionscript.info
> User-Agent: curl/7.65.3
> Accept: */*
> Cookie: session=eyJjbGllbnRfaWQiOjEwOCwidXNlcl9pZCI6MjgxfQ.Xc2ztw.Cmn6G2MTGe0XvoWD31mt2Gy0pvk
> Content-Type: application/json
> Content-Length: 111
> 
* upload completely sent off: 111 out of 111 bytes
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx
< Date: Thu, 14 Nov 2019 20:08:00 GMT
< Content-Type: application/json
< Content-Length: 83
< Connection: keep-alive
< 
{"email":"ryan@educatethewait.com","uuid":"0221e40a-83d8-4884-a488-1f35c72023c4"}

```

---

# Login

**Route:** `/auth/login`

**Arguments:**

- email (example: ryan@getmediapanel.com)
- password (example: Password01)
  - Must contain: one capital letter, one lowercase letter
  - Must be at least 6 characters, at most 64

**Returns:**

- email: Email used to log in
- uuid: UUID4 used to identify the client

**Errors:**

HTTP 401: Username or password incorrect.

**Example:**

```
# curl -v -XPOST https://beta.mediapanel.fusionscript.info/auth/login \
 -d'{"email": "ryan@educatethewait.com", "password": "Password01"}' \
 -H "Content-Type: application/json"

> POST /auth/login HTTP/1.1
> Host: beta.mediapanel.fusionscript.info
> User-Agent: curl/7.65.3
> Accept: */*
> Content-Type: application/json
> Content-Length: 65
> 
* upload completely sent off: 65 out of 65 bytes
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx
< Date: Thu, 14 Nov 2019 20:05:33 GMT
< Content-Type: application/json
< Content-Length: 82
< Connection: keep-alive
< Vary: Cookie
* Added cookie session="eyJjbGllbnRfaWQiOjEwOCwidXNlcl9pZCI6MjgxfQ.Xc2zjQ.Bq_KdjobFpnexGrfCBQKJ1XZa74" for domain beta.mediapanel.fusionscript.info, path /, expire 0
< Set-Cookie: session=eyJjbGllbnRfaWQiOjEwOCwidXNlcl9pZCI6MjgxfQ.Xc2zjQ.Bq_KdjobFpnexGrfCBQKJ1XZa74; HttpOnly; Path=/
< 
{"email":"ryan@educatethewait.com","uuid":"da0a781a-cda5-401e-9b35-c4cb28192e96"}
```
