create virtual enviroment
`py -3 -m venv venv`

run venv
`venv\Scripts\activate`

install fastapi full
`pip install fastapi[all]`

run fastapi server
`uvicorn main:app --reload`

`uvicorn app.main:app --reload`

create hex random number on bash for secret key
`openssl rand -hex 32`

Initialize alembic
`alembic init [folder name]`

Make migration on database with revision
`alembic revision -m [message]`

Run the migration
`alembic upgrade [revision number]`

**Note:** 1. deprecated bycrypt
