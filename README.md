# Drones API

Drones project simmulating how drones can be loaded with medications, taking into account bussiness rules declared on STUDY_CASE.md

## Installation

- Install python stable version [python](https://www.python.org/downloads/).

- Create virtualenv

```bash
python -m venv venv
```

- Activate virtualenv

- Install dependencies

```bash
pip install -r requirements.txt
```

## Env variables

- Setup environment variables on **.env** file. You should change SECRET_KEY, here you can create a new one 
[Secret Key Generator](https://djecrety.ir/) 

- Create database tables and load data to it

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata drones, medications
```

## Database settings

- Run project to test configurations and auto-create database

```bash
python manage.py runserver
```

- Create database tables and load data to it

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata drones, medications
```

- Run the next command to add scheduled task to database

```bash
python manage.py crontab add
```

> If you get an error, ensure you are building the project on linux based system, because it has a library that is not 
compatible with Windows OS

- Create superuser to access django admin panel

```bash
python manage.py createsuperuser
```

> If you want to create new data on the database, access admin panel and create Mediactions or use register method to 
create new Drones 

## Documentation
Access [Drones API Site](http://127.0.0.1/docs/) to see endpoints and description. 

## Architecture assumptions
Read **ARCHITECTURE.md** file to understand the assumptions made on the design process of the project
