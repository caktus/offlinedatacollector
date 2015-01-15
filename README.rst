

Offlinedatacollector
========================

Below you will find basic setup and deployment instructions for the offlinedatacollector
project. To begin you should have the following applications installed on your
local development system::

- Python >= 3.4
- `pip <http://www.pip-installer.org/>`_ >= 1.5
- `virtualenv <http://www.virtualenv.org/>`_ >= 1.10
- `virtualenvwrapper <http://pypi.python.org/pypi/virtualenvwrapper>`_ >= 3.0
- Postgres >= 9.1
- git >= 1.7


Getting Started
------------------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv offlinedatacollector -p `which python3.4`
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::

    cp offlinedatacollector/settings/local.example.py offlinedatacollector/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=offlinedatacollector.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon offlinedatacollector

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 offlinedatacollector
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Deployment
------------------------

You can deploy changes to a particular environment with
the ``deploy`` command::

    fab staging deploy

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.
