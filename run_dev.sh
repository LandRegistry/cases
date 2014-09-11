#!/bin/bash

./db/upgrade_database.sh
foreman start -f Procfile-dev
