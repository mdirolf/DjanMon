=======
DjanMon
=======
:Author: Mike Dirolf <mike@10gen.com>

About
=====
DjanMon is a demo showing how to use MongoDB and PyMongo from a Django
project.

As of this writing there is no support for using MongoDB as a
**django.db** backend. There is at least `one project
<http://bitbucket.org/kpot/django-mongodb/>`_ trying to implement this
type of direct support for Django, although `some people
<http://simonwillison.net/2009/Jun/30/mongodb/#c46834>`_ disagree with
that approach.

This project is an attempt to show how MongoDB can be used from within
a Django project even without **django.db** support.

MongoDB and Django
==================
Since Django models don't work with MongoDB, you'll need to disable
the authentication, admin and sessions components (all of which depend
on Django models) in *settings.py*. You should also leave all of the DATABASE_*
settings set to the empty string. The relevant sections of
*settings.py* should look something like the following::

  DATABASE_ENGINE = ''
  DATABASE_NAME = ''
  DATABASE_USER = ''
  DATABASE_PASSWORD = ''
  DATABASE_HOST = ''
  DATABASE_PORT = ''

  MIDDLEWARE_CLASSES = (
      'django.middleware.common.CommonMiddleware',
  #    'django.contrib.sessions.middleware.SessionMiddleware',
  #    'django.contrib.auth.middleware.AuthenticationMiddleware',
  )

  INSTALLED_APPS = (
  #    'django.contrib.auth',
      'django.contrib.contenttypes',
  #    'django.contrib.sessions',
      'django.contrib.sites',
  )

Also, keep in mind you won't need to use *manage.py* to sync your database
like you normally would with Django - MongoDB is schema-free!

Dependencies
============
You'll need Django, MongoDB and PyMongo installed to run DjanMon.
