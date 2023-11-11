- [Letter](#letter)
  - [Métodos permitidos](#métodos-permitidos)
  - [Index](#index)
    - [Registro](#registro)
      - [Erros](#erros)
  - [User](#user)
    - [POST](#post)
      - [Erros](#erros-1)
    - [Delete](#delete)
      - [Erros](#erros-2)
  - [Detalhe](#detalhe)
    - [GET](#get)
      - [Erros](#erros-3)
    - [DELETE](#delete-1)
      - [Erros](#erros-4)


# Letter

Letter é a rota da api responsável por gerenciar operações relacionadas às cartas.

## Métodos permitidos

**GET | POST | DELETE**

## Index

    http://{host}/api/letter

### Registro

**POST**

Usado para registrar novas cartas.

Em caso de sucesso, retorna uma mensagem de sucesso.

Modelo json: 

    {
        "username": "text", // Username from registered user
        "date": "date", // Date from letter. **Optional field**
        "sender": "text", // Letter sender
        "text": "ABC", // Letter text
    }

Exemplo python:

    from requests import post

    url = "http://{host}/api/letter"

    data = {
        "username": "username",
        "date": "01-01-2000",
        "sender": "Anonymous",
        "text": "ABC",
    }

    response = post(url, data=data)

Exemplo javascript (fetch):

    const url = "http://{host}/api/letter"
    const data = {
        "username": "username",
        "date": "01-01-2000",
        "sender": "Anonymous",
        "text": "ABC",
    }

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Retorno**:

    {
        res: "Letter sent successfully"
    }

#### Erros

*Username* inválido:

    {
        detail: "Username is not valid"
    }

## User

User é responsável por gerenciar as cartas recebidas pelo usuário.

    http://{host}/api/letter/user/

**POST | DELETE**

### POST

**POST**

Irá retornar as cartas recebidas pelo usuário.

Caso não seja o limite de cartas não seja informado, será retornada as 20 primeiras cartas recebidas.

Modelo json: 

    {
        "username": "text", // Username from registered user
        "token": "text" // Token from registered user,
        "index-init": "number", // Init to list the letters [optional]
        "index-end": "number", // End to list the letters [optional]
        "index-all": "boolean" // List all letters [optional]
    }

**Nota:** Caso o parâmetro *"index-all"* seja definido como *true*, a api retornará todas as letters do usuário.

Exemplo python:

    from requests import post

    url = "http://{host}/api/letter/user/"

    data = {
        "username": "username",
        "token": "text",
        "index-init": 0,
        "index-end": 5
    }

    response = post(url, data=data)

    # All

    data = {
        "username": "username",
        "token": "text",
        "index-all": true
    }

    response = post(url, data=data)

Exemplo javascript (fetch):

    const url = "http://{host}/api/letter/user"
    const data = {
        "username": "username",
        "token": "text",
        "index-init": 0,
        "index-end": 5
    }

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

    // All

    data = {
        "username": "username",
        "token": "text",
        "index-all": true
    }

    const response = fetch(url, { 
        method: "POST",
        body: JSON.stringify(data),
        headers: { 
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**RETORNO**

Retorna uma lista com objetos, contendo as cartas recebidas pelo usuário.

    [
        {
            "date": "date",
            "sender": "text",
            "text": "text",
            "letter_token": "text"
        }
    ]

#### Erros

*Username* ou *token* inválidos:

    {
        "detail": "Username or token is not valid"
    }

### Delete

Irá deletar **todas** as cartas recebidas pelo usuário.

Modelo json: 

    {
        "username": "text", // Username from registered user
        "token": "text" // Token from registered user
    }

Exemplo python:

    from requests import delete

    url = "http://{host}/api/letter/user/"

    data = {
        "username": "username",
        "token": "text"
    }

    response = delete(url, data=data)

Exemplo javascript (fetch):

    const url = "http://{host}/api/letter/user"
    const data = {
        "username": "username",
        "token": "text"
    }

    const response = fetch(url, {
        method: "DELETE",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json());

**Retorno**

    {
        "res": "Letters deleted!"
    }

#### Erros

*Username* ou *token* inválidos:

    {
        "detail": "Username or token is not valid"
    }

## Detalhe

Serve para gerenciar dados específicos a uma carta.

    http://{host}/api/letter/detail/<letter_token>/

**GET | DELETE**

### GET

Retorna as informações da carta

Exemplo python:

    from requests import get

    response = get("http://{host}/api/letter/detail/<letter_token>/")

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/letter/detail/<letter_token>/", {
        method: "GET"
    }).then(response => response.json());

**Retorno:** 

    {
        "username": "text",
        "date": "date",
        "text_path": "text",
        "sender": "text",
        "letter_token": "text",
        "text": "text"
    }

#### Erros

*Token* inválido:

    {
        "res": "Letter don't exists"
    }

### DELETE

Serve para deletar a carta.

Exemplo python:

    from requests import delete

    response = delete("http://{host}/api/letter/detail/<letter_token>/")

Exemplo javascript (fetch):

    const response = fetch("http://{host}/api/letter/detail/<letter_token>/", {
        method: "DELETE"
    }).then(response => response.json());

**Retorno**

    {
        res: "Letter deleted!"
    }

#### Erros

*Token* inválido:

    {
        "res": "Letter don't exists"
    }