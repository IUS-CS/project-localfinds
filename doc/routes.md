# LocalFinds - Routes

## Posts

### **/**

View all posts

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK

### **/posts/create**

Create a post (requires login)

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 403 Unauthorized

### **/posts/\<id>**

View a post

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 404 Not Found

### **/posts/\<id>/edit**

Edit a post (owner only)

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 403 Unauthorized
- 404 Not Found

### **/posts/\<id>/delete**

Delete a post (owner/admin)

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 403 Unauthorized
- 404 Not Found

### **/posts/search?q=term**

Search posts

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK

## Accounts

### **/accounts/create**

Register

- Usernames are unique and limited to 15 characters.
- Passwords are hashed using Werkzeug.

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK

### **/accounts/\<username>**

View profile

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 404 Not Found

### **/accounts/\<username>/edit**

Edit account (owner)

- Usernames are unique and limited to 15 characters.
- Passwords are hashed using Werkzeug.
- Admin account cannot be modified.

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 400 Bad Request
- 403 Unauthorized
- 404 Not Found

### **/accounts/\<username>/delete**

Delete account and all assosiated posts (owner/admin).

- Admin account cannot be deleted.

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
- 403 Unauthorized
- 404 Not Found

## Authentication

### **/auth/login**

Login

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK

### **/auth/logout**

Logout

#### Verbs

- GET
- POST

#### Response Codes

- 200 OK
