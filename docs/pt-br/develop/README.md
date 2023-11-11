- [Desenvolvimento](#desenvolvimento)
  - [Env](#env)
  - [Docker](#docker)
  - [Settings](#settings)
- [Database](#database)
- [Executando](#executando)
- [Testes](#testes)


# Desenvolvimento

Certifique-se de ter o *docker* e o *docker-compose* instalados.

Navegue até a pasta da api

## Env

Copie o *.env_example* e crie um arquivo chamado de *.env*, ele irá configurar as variáveis de ambiente.

*ALLOWED_HOSTS*: Hosts que podem acessar a api, escreva sem o uso de aspas e separando os hosts por vírgula

    ALLOWED_HOSTS=localhost, abc, foo, bar

## Docker

Faça a build:

    docker-compose build

Execute o container:

    docker-compose up -d

Execute o bash no container:

    docker container exec -it api_api_1 bash

Navegue até a pasta *main* e execute o setup.py

    python setup.py

Ele irá criar uma copia de *settings_example* ou restaurar o *settings* caso haja um backup dele, criar a *database*, pasta para armazenamento das *letters*, configurações de criptografia.

Em suma, o *setup* permite a configuração automática de tudo necessário para a execução do programa.

**Nota:** Em *database/backups* você pode encontrar uma cópia de *settings.py*, isso existe para fazer um backup das chaves de criptografia, dessa forma, caso seja necessário reiniciar o *container*, ele irá automaticamente restaurar as chaves, desse modo, a *database* não será inutilizada.

## Settings

Para o desenvolvimento, pode-ser útil a visualização dos dados no navegador, para isso comente a linha *DEFAULT_RENDERER_CLASSES*

    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        # "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
        "PAGE_SIZE": 10,
    }

# Database

Navegue para a raiz do projeto

    cd ..

Faça a migração da base de dados

    python manage.py migrate

Crie o super usuário

    python manage.py createsuperuser

# Executando

Para executar o projeto, você deve usar o seguinte comando:

    python manage.py runserver 0.0.0.0:8000

Isso fará ele ser exposto na porta 8000, conforme determinação do *Dockerfile*.

Assim, para acessar a api basta acessar:

    http://localhost:8000/api

# Testes

Para ter certeza do funcionamento da api, execute os testes:

    python manage.py test api/tests/

Caso não seja retornado nenhum erro, é um sinal de que a api está pronta para uso.