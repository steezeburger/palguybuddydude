# Django w/ Postgres starter

* git clone the repo to your machine
* find and replace instances of `yourproject` with the name of your project
* `$ cd packages/django-app`
* `python -m venv .venv`
  * not technically necessary, but useful for installing locally to add pip packages and update the requirements.txt file
  * `$ source .venv/bin/activate`
  * `$ pip install pipenv`
  * `$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --deploy`
  * `$ pipenv install some_package`
* `$ cp .env.template .env`
* `$ docker-compose build`
* `$ ./utils/create-docker-volumes.sh`
* `$ ./bin/dcp-generate-secret-key.sh`
  * copy and paste the output from this command into `.env` replacing `SECRET_KEY_GOES_HERE`
* `$ ./bin/dcp-django-admin.sh migrate`

* now, you have two options
  * create your own superuser
    * `$ ./bin/dcp-django-admin.sh createsuperuser`
  * load db w/ user admin@email:password
    * `$ ./utils/reload-docker-db.sh --data=dev_data.json`

* `$ docker-compose up web`
* you can now login with your superuser at 0.0.0.0:8000/admin

## helpful scripts
* `$ ./utils/dcp-run-tests.sh`
  * runs all tests, except those decorated with `@pytest.mark.integration`
  * tests.py test_*.py *_test.py *_tests.py
* `$ ./bin/dcp-django-admin.sh`
  * runs `manage.py` in the docker container with argument passthrough
  * `$ ./bin/dcp-django-admin.sh makemigrations`
  * `$ ./bin/dcp-django-admin.sh migrate`
  * `$ ./bin/dcp-django-admin.sh startapp payments`
* `$ ./utils/reload-docker-db.sh`
  * reloads `dev_data.json` by default
  * `$ ./utils/reload-docker-db.sh --data=fixture_filename.json`
* `$ ./utils/dump-data.sh`
  *  `$ ./utils/dump-data.sh > app/core/fixtures/dump-2021-10-08.json`
  * you can then reload these files with `./utils/reload-docker-db.sh`
