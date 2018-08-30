# scorecard

This application will import and display data taken from the https://github.com/ComplianceAsCode/redhat project.

See http://atopathways.redhatgov.io/product-documents/ for a similar effort.

See also:
https://github.com/opencontrol
https://github.com/RedHatGov/ato-pathways

This initial Django project was created by doing:
```
mkdir -p ~/.virtenvs
virtualenv ~/.virtenvs/scorecard --python python3.6
source ~/.virtenvs/scorecard/bin/activate
pip install Django PyYAML psycopg2 gunicorn django-debug-toolbar
pip freeze > requirements.txt
./manage.py startapp scorecard
```
