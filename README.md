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

Upgrade by step
`alembic upgrade [+n step]`

Show current revision
`alembic current`

Show updated revision
`alembic head`

Run updated revision
`alembic upgrade head`

Rollback with revision
`alembic downgrade [revision number]`

Rollback by step
`alembic downgrade [-n step]`

Auto create revision from model
`alembic revision --autogenerate -m [message]`

**Note:** 1. deprecated bycrypt
