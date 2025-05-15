# DSP-project
This project contains the prototype related to the project of group F2.

The application uses the following technologies:
- FastAPI as framework for the backend
- Uvicorn as an ASGI web server
- SQLAlchemy for database communication
- Alembic for databas migrations
- React as framework for the frontend

## Installation
For Linux (Ubuntu LTS) and MacOS.

The project can be easily configured with poetry and npm for package control.

### Install Docker and Docker-Compose
Docker and Docker-Compose are both useful for running the application but not
necessary. It is used to setup the database easily and provide a database interface.

Start by installing Docker CE (Community Edition) by going [here](https://docs.docker.com/install/) and selecting your
 operating system in the menu on the left.

To install docker-compose, please follow the instructions [here](https://docs.docker.com/compose/install/).

### NodeJS
To install NodeJS for Linux, we recommend the latest LTS version of Node. The latest LTS version is listed on the [homepage of NodeJS](https://nodejs.org/en/). To install, follow the instructions [here](https://github.com/nodesource/distributions/blob/master/README.md). Make sure to install the LTS version.

For MacOS, `brew install node` should be sufficient.

### Poetry
For Linux and MacOS, run `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -`.

---
## Database
For the database, docker images are used. Create a .env file in the root of the project containing the following environment variables:

POSTGRES_PASSWORD={pwd} \
POSTGRES_DB=rtls-visualistion \
POSTGRES_USER= {username} \
POSTGRES_HOST=localhost \
POSTGRES_PORT=5432 -> set to port in docker-compose.yml for development through docker\
MQTT_BROKER_URL=chimay.science.uva.nl \
MQTT_BROKER_PORT=8020 \
MQTT_TOPIC=uva_test/pos \
DEBUG=True \

Run the migrations in the backend to update the database

```cd backend```

```alembic upgrade head```

The database can then be started by running in the root of the project:

```docker-compose up```

To verify that the database has been setup correctly, go to `adminer` at.

```http://localhost:8080```

Here, login using the following (the Database field should be empty):
```
System: PostgreSQL
Server: database
Username: {username}
Password: {pwd}
Database:
```

Now verify that the database `rtls-visualistion` exists and contains the tables.
The database can also be setup without docker. Then follow the
[documentation](https://www.postgresql.org/docs/15/) of postgres. Alembic should work accordingly.

## Backend
The backend can be built using poetry to install all dependencies. The use
of virtual environment is encouraged, for example using poetry as in this setup, but a regular python virtual environment would work as well.

```cd backend```

```poetry install```

In the root .env file some other variables need to be set, if not done yet, namely with:

MQTT_BROKER_URL=chimay.science.uva.nl
MQTT_BROKER_PORT=8020
MQTT_TOPIC=uva_test/pos

To use the broker on the chimay server, other local MQTT brokers can be used as well. Furthermore

DEBUG=True

To set CORS policies for the backend. The backend can then be initiated inside its folder by running:

```uvicorn app:app --host {host} --port {port} --reload```

To run the application in the poetries virtual environment:

```poetry shell```

To activate the environment and than running the command above or use:

```poetry run uvicorn app:app --host {host} --port {port} --reload```

## Frontend
The frontend can be built by using npm to install all dependencies.

```cd frontend```

```npm install```

Also an .env file in the frontend folder needs to be created with the urls and port to the backend for the API's and Sockets:

REACT_APP_FRONTEND_API_URL=http://{url}:{port}
REACT_APP_FRONTEND_WS_URL=ws://{url}:{port}

The frontend than can be started inside its folder by running:

```npm start```
