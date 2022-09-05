Bankey development Installation
====================================================

Install requirements
-------------------------

Install `Poetry` for managing dependencies:

```
brew install poetry
```


Install dependencies (based od `poetry.lock` file)

```
poetry install
```

> Run `poetry shell` for activating virtual environment



Create a new database or use existing one
--------------

Project contains small sqllite3 database, `db.sqllite3`.

If you don't want to user existing database, you can create you own.

First, create migrations files:

```
poetry run python manage.py makemigrations
```

Second, migrate changes:

```
poetry run python manage.py migrate
```


Runing Application on Development Server
------------------

If you would like to check if everything is working correctly, run tests:


```
poetry run pytest core/tests.py
```

You can also run development server:

```
poetry run python manage.py runserver
```

Server will run on `http://localhost:8000/` with small UI app.
