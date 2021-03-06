Installing PostgreSQL on Fedora 17
##################################
:tags:  linux

With the new systemd this now requires a couple of manual steps.

Obviously we start by installing the RPMS themselves:

::

    sudo yum install postgresql-server postgresql

If you were to now try and start the server it would fail as there is no
database. The old SysV init script had an *initdb* option, but this no
longer exists in the systemd service script. This means that you need to
initialise the database manually:

::

    sudo -u postrgres initdb -D /var/lib/pgsql/

You can now start the service and enable it permanently

::

    sudo service postgresql start
    sudo chkconfig postgresql on

Now you can enter the database as the postgres *superuser*:

::

    sudo -u postgres psql -d postgres

Finally create your user and associated database

::

    CREATE ROLE "testAdmin" LOGIN PASSWORD 'testAdmin';
    CREATE DATABASE "testDB" WITH ENCODING='UTF8' OWNER="testAdmin";
    \q

