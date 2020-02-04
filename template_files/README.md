APPHEADER_LINE
APPNAME
APPHEADER_LINE

APPNAME description

Quick start
-----------

1. `pip install` the app
    - Local: `pip install -e /path/to/APPNAME/repo`

2. Add "APPNAME" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'APPNAME',
    ]

3. Include the APPNAME URLconf in your project urls.py like this::

    path('APPNAME/', include('APPNAME.urls')),

4. Run `python manage.py migrate` to create the APPNAME models.
