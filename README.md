# ctfspace: Jeopardy-style CTF Hosting Platform
ctfspace is an jeopardy-style CTF hosting platform.  
Initially written for 2016 Layer7 CTF, it was also used in 2017 SECUINSIDE CTF and 2017 CHRISTMAS CTF.

## Features
* Basic challenge-auth system 
* Dashboard & Notice panel
* Real-time ranking view
* Dynamic score adjustment based on solver count

## Getting started
Create virtualenv using your preferred method (we're using classic `virtualenv`)
```sh
$ virtualenv -p python3 venv
```

Activate virtualenv:
```bash
$ source venv/bin/activate
```

Install required dependencies:
```sh
$ pip install -r requirements.txt
```

Create local settings:
```sh
$ cp ctfspace/settings/local_frank.py ctfspace/settings/local_$USER.py
```

Build & apply migrations:
```sh
$ python manage.py makemigrations accounts challenges notice
$ python manage.py migrate
```
(By default the project uses SQLite backend; you can change this in settings)

(Optional) Create superuser:
```sh
$ python manage.py createsuperuser
```
When asked for Age type, use 4 (Age.OTHER).

Start the development server:
```sh
$ python manage.py runserver
```
Server is now available at http://127.0.0.1:8000/.

## Notes about the dynamic score adjustment
Some constants are currently hardcoded & described in `challenges/models.py`. More description about the parameters is available at https://www.desmos.com/calculator/vl5yx8rsq6.