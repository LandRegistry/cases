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
export MINT_URL='http://mint.landregistry.local'
```

Note in local dev port is assigned by dev env scripts, so in production assign a port.

For production
```
PORT=[SOME NUMBER]
SETTINGS='config.Config'
export DATABASE_URL='postgresql://user:password@db_host:port:db_name'
export DECISION_URL='http://decision_host'
export MINT_URL='http://mint_host'
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


##### Create Debian package

```
cd packaging
./build.sh
```

This will create a virtualenv, install cases into that env. Then it will set virtualenv paths to match the eventual installation directory of the debian package that is the output of build.sh.

**Note**
The packaging of a virtualenv using fpm may soon be much easier depending on [outcome of this](https://github.com/jordansissel/fpm/issues/697)

The result of running ./build.sh is debian package will be created in packaging called cases. The package has a basic upstart config, empty pre and post install and remove scripts. For the moment the installer is set to install to /opt/alpha/cases. Change as required. Also post install does not set ownership or permissions on the installed package.

The deb package also contains the two runnable worker processes that process pending and approved changes. There are upstart configs for both of the worker processes.

**Before installing in a production box you should:**

* Set the environment variables as listed in environnment.sh **(put the file into the package install dir - have config management tool do this)**
* Create a no login user account that the matching service can be owned by and run as (at the moment in a dev vagrant it runs as root)

##### To install the debian package

```
sudo dpkg -i cases_0.1_all.deb
```

Then run

```
sudo start cases
sudo start pending-cases
sudo start process-cases
```

Note that this assumes you have set all the correct environment variables.

To uninstall

```
sudo dpkg -r cases
```

##### Database migrations

At the moment the migration version files and manage.py are included in packages and live in installation directory. I would for the moment run these after the install (and under control of configuration management tool) before running the service.

```
cd /opt/alpha/cases
python manage.py db upgrade
```
