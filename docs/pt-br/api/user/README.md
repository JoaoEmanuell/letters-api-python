- [User](#user)
  - [Métodos permitidos](#métodos-permitidos)
  - [Index](#index)
    - [Registro](#registro)
    - [Erros](#erros)
  - [Detalhes](#detalhes)
    - [GET](#get)
    - [PUT](#put)
    - [Erros](#erros-1)
    - [DELETE](#delete)
    - [Erros](#erros-2)
  - [Login](#login)
    - [Erros](#erros-3)
  - [Username](#username)
    - [GET](#get-1)


# User

User é a rota da api responsável por gerenciar operações relacionadas aos usuários.

## Métodos permitidos

**GET | POST | PUT | DELETE**

## Index

    http://{host}/api/user

### Registro

**POST**

Usado para registrar novos usuários no sistema.

Em caso de sucesso, retorna o token do usuário.

Modelo json:

    {
        "name": "text", 
        "username": "text", 
        "password": "text"
    }

Exemplo python:

    from requests import post

    data = {"name": "test", "username": "test", "password": "test"}

    response = post("http://{host}/api/user", data=data)

Exemplo javascript (fetch):

    const url = "http://{host}/api/user"
    const data = {"name": "test", "username": "test", "password": "test"}

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());


**Retorno:**

    {
        "token": "$2b$08$A3nFpxON3N2KcTrHiwtreNNrfoMgSuRxEA5eq6UIZdOA7GGXpZGa"
    }

### Erros

*Username* repetido:

    {
        "username":["user with this username already exists."]
    }

Campo muito longo:

    {
        "field": ["Ensure this field has no more than {xx} characters."]
    }

## Detalhes

    http://{host}/api/user/detail/<token>

**GET**, **PUT**, **DELETE**

### GET

**GET**

Retorna os dados do usuário

Exemplo python:

    from requests import get

    response = get("http://{host}/api/user/detail/<token>")

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "GET"
    }).then(response => response.json());

**Retorno:** 

    {
        "name": "name",
        "username": "username"
    }

### PUT

**PUT**

Permite a edição dos dados do usuário

Modelo json:

    {
        "name": "text", // Optional
        "username": "text", // Optional
        "password": "text" // Optional
    }

Exemplo python:

    from requests import put

    data = {"name": "name"}

    response = put("http://{host}/api/user/detail/<token>", data=data)

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "PUT",
        body: JSON.stringify({"name": "name"}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Retorno:**

    {
        res: "Successfully changed user data"
    }

### Erros

*Username* repetido:

    {
        "username":["user with this username already exists."]
    }

Campo muito longo:

    {
        "field": ["Ensure this field has no more than {xx} characters."]
    }


### DELETE

Permite deletar um usuário.

Além disso, deleta todas as cartas que o usuário recebeu.

Exemplo python:

    from requests import delete

    response = delete("http://{host}/api/user/detail/<token>")

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/user/detail/<token>", {
        method: "DELETE"
    }).then(response => response.json());

**Retorno:**

    {
        "res": "User deleted!"
    }

### Erros

*Usuário não existe*

    {
        "res": "User don't exists"
    }

*Ocorre quando o token passado é inválido.*

## Login

    http://{host}/api/user/login/

**POST**

Permite ao usuário logar no sistema.

Modelo json:

    {
        "username": "text",
        "password": "text"
    }

Exemplo python:

    from requests import post

    data = {"username": "test", "password": "test"}

    response = post("http://{host}/api/user/login/", data=data)

Exemplo javascript (fetch):

    const url = "http://{host}/api/user/login/"
    const data = {"username": "test", "password": "test"}

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Retorno:**

    {
        "token": "$2b$08$A3nFpxON3N2KcTrHiwtreNNrfoMgSuRxEA5eq6UIZdOA7GGXpZGa"
    }

### Erros

*Usuário não existe*

    {
        "res": "User don't exists"
    }

*Ocorre quando o username passado é inválido.*

****

*Senha inválida*

    {
        res: "Invalid password"
    }

*Ocorre quando a senha passada é inválida*

## Username

    http://{host}/api/user/username/<username>

### GET

**GET**

Retorna se o usuário está registrado

Exemplo python:

    from requests import get

    response = get("http://{host}/api/user/username/<username>")

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/user/username/<username>", {
        method: "GET"
    }).then(response => response.json());

**Retorno:**

Caso o usuário exista:

    {
        "res": true
    }

Caso o usuário não exista:

    {
        "res": false
    }