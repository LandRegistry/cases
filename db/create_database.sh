#!/bin/bash

createuser -s cases
createdb -U cases -O cases cases -T template0