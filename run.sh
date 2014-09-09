source ./environment.sh

set +o errexit
createuser -s cases
createdb -U cases -O cases cases -T template0

python manage.py db upgrade
python run_dev.py