# Here we'll create a test database, and override the database to the test values.
set +o errexit
createuser -s cases_test
createdb -U cases_test -O cases_test cases_test -T template0
set -e

export SETTINGS='config.TestConfig'
export DATABASE_URL='postgresql://localhost/cases_test'
export DECISION_URL='http://nowhere'
export MINT_URL='http://nowhere/'
export SEARCH_URL='http://nowhere/'
