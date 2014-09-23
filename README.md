cases
=====

[![Build Status](https://travis-ci.org/LandRegistry/cases.svg)](https://travis-ci.org/LandRegistry/cases)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/cases.svg)](https://coveralls.io/r/LandRegistry/cases)


The service to handles cases. Cases refers to an application and the relevant documentation lodged at Land Registry to be processed (such as 'register a charge') from a citizen/conveyancer


### Getting started

```
git clone git@github.com:LandRegistry/cases.git
cd cases
```

#### Run tests

```
pip intall -r test_requirements.txt
```

Then run:

```
py.test
```

### Environment variables needed

```
SETTINGS
DATABASE_URL
DECISION_URL
MINT_URL
```

Local development config:

```
export SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql://localhost/cases'
export DECISION_URL='http://decision.landregistry.local'
export MINT_URL='http://mint.landregistry.local/'
```

#### Create/Update database

There's an intial migration script in the project created using Flask-Migrate so you just need to call the following

```
python manage.py db upgrade
```

On heroku run this
```
heroku run python manage.py db upgrade --app lr-cases
```

Run the upgrade command whenever you have additional migrations

### Run the app

Run in dev mode to enable app reloading

```
dev/run-app
```

Run tests

```
dev/run-unit-tests
```

** This app runs on PORT 8014
