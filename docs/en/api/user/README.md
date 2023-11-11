- [User](#user)
  - [Methods allowed](#methods-allowed)
  - [Index](#index)
    - [Record](#record)
    - [Errors](#errors)
  - [Details](#details)
    - [GET](#get)
    - [PUT](#put)
    - [Errors](#errors-1)
    - [DELETE](#delete)
    - [Errors](#errors-2)
  - [Login](#login)
    - [Errors](#errors-3)


# User

User is the api route responsible for managing operations related to users.

## Methods allowed

**GET | POST | PUT | DELETE**

## Index

    http://{host}/api/user

### Record

**POST**

Used to register new users in the system.

On success, it returns the user's token.

json template:

    {
        "name": "text", 
        "username": "text", 
        "password": "text"
    }

Python example:

    from requests import post

    data = {"name": "test", "username": "test", "password": "test"}

    response = post("http://{host}/api/user", data=data)

Example javascript (fetch):

    const url = "http://{host}/api/user"
    const data = {"name": "test", "username": "test", "password": "test"}

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());


**Return:**

    {
        "token": "$2b$08$A3nFpxON3N2KcTrHiwtreNNrfoMgSuRxEA5eq6UIZdOA7GGXpZGa"
    }

### Errors

*Username* repeated:

    {
        "username":["user with this username already exists."]
    }

Field too long:

    {
        "field": ["Ensure this field has no more than {xx} characters."]
    }

## Details

    http://{host}/api/user/detail/<token>

**GET**, **PUT**, **DELETE**

### GET

**GET**

Returns user data

Python example:

    from requests import get

    response = get("http://{host}/api/user/detail/<token>")

Example javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "GET"
    }).then(response => response.json());

**Return:**

    {
        "name": "name",
        "username": "username"
    }

### PUT

**PUT**

Allows editing of user data

json template:

    {
        "name": "text", // Optional
        "username": "text", // Optional
        "password": "text" // Optional
    }

Python example:

    from requests import put

    data = {"name": "name"}

    response = put("http://{host}/api/user/detail/<token>", data=data)

Example javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "PUT",
        body: JSON.stringify({"name": "name"}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Return:**

    {
        res: "Successfully changed user data"
    }

### Errors

*Username* repeated:

    {
        "username":["user with this username already exists."]
    }

Field too long:

    {
        "field": ["Ensure this field has no more than {xx} characters."]
    }


### DELETE

Allows you to delete a user.

In addition, it deletes all cards that the user received.

Python example:

    from requests import delete

    response = delete("http://{host}/api/user/detail/<token>")

Example javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "DELETE"
    }).then(response => response.json());

**Return:**

    {
        "res": "User deleted!"
    }

### Errors

*User does not exist*

    {
        "res": "User don't exists"
    }

*Occurs when the token passed is invalid.*

## Login

    http://{host}/api/user/login/

**POST**

Allows the user to log into the system.

json template:

    {
        "username": "text",
        "password": "text"
    }

Python example:

    from requests import post

    data = {"username": "test", "password": "test"}

    response = post("http://{host}/api/user/login/", data=data)

Example javascript (fetch):

    const url = "http://{host}/api/user/login/"
    const data = {"username": "test", "password": "test"}

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Return:**

    {
        "token": "$2b$08$A3nFpxON3N2KcTrHiwtreNNrfoMgSuRxEA5eq6UIZdOA7GGXpZGa"
    }

### Errors

*User does not exist*

    {
        "res": "User don't exists"
    }

*Occurs when the username passed is invalid.*

****

*Invalid password*

    {
        res: "Invalid password"
    }

*Occurs when the password passed is invalid*