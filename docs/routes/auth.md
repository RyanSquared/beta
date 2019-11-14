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
