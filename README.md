Copyright 2020 Mario Reichel

# companynetworkmanager
Manage your IT: take inventory of your devices and mold you network

## Start Test Environment

* Make your own settings.py, like settings_priv.py
* set new default settings file

`export DJANGO_SETTINGS_MODULE=companymanager.settings_priv`
* Start Server with python3 manage.py runserver

## Steps to install
* download repository
* copy default config files and change them
* `docker-compose build`
* `docker-compose up -d`
    or without -d for debugging
* create superuser by 'docker exec -it <id> python manage.py createsuperuser'
