#!/bin/bash

set -x
set -e

createuser -s cases
createdb -U cases -O cases cases -T template0
