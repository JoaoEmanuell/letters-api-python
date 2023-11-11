- [Development](#development)
  - [Env](#env)
  - [Docker](#docker)
  - [Settings](#settings)
- [Data base](#data-base)
- [Running](#running)
- [Tests](#tests)


# Development

Make sure you have *docker* and *docker-compose* installed.

Navigate to the api folder

## Env

Copy the *.env_example* and create a file called *.env*, it will configure the environment variables.

*ALLOWED_HOSTS*: Hosts that can access the api, write without using quotes and separating the hosts by a comma

    ALLOWED_HOSTS=localhost, abc, foo, bar

## Docker

Make the build:

    docker-compose build

Run the container:

    docker-compose up -d

Run bash in the container:

    docker container exec -it api_api_1 bash

Navigate to the *main* folder and run setup.py

    python setup.py

It will create a copy of *settings_example* or restore *settings* if there is a backup of it, create the *database*, folder for storage of *letters*, encryption settings.

In short, *setup* allows automatic configuration of everything necessary for running the program.

**Note:** In *database/backups* you can find a copy of *settings.py*, this is there to make a backup of the encryption keys, that way if you need to restart the *container* it will automatically restore the keys, that way the *database* will not be rendered useless.

## Settings

For development, it may be useful to visualize the data in the browser, for that, comment out the line *DEFAULT_RENDERER_CLASSES*

    REST_FRAMEWORK = {
       "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
       # "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
       "PAGE_SIZE": 10,
    }

# Data base

Navigate to the project root

    cd ..

Migrate the database

    python manage.py migrate

Create the super user

    python manage.py createsuperuser

# Running

To run the project, you must use the following command:

    python manage.py runserver 0.0.0.0:8000

This will cause it to be exposed on port 8000, as determined by the *Dockerfile*.

So, to access the api just access:

    http://localhost:8000/api

# Tests

To make sure the api works, run the tests:

    python manage.py test api/tests/

If no error is returned, it is a sign that the api is ready to use.