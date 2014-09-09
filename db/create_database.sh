#!/bin/bash

set -x
createuser -s cases
createdb -U cases -O cases cases -T template0
