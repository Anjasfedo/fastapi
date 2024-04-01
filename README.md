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

**Note:** 1. deprecated bycrypt
