{app_header_line}
{app_name}
{app_header_line}

{app_name} description

Quick start
-----------

1. `pip install` the app
    - Local: `pip install -e /path/to/{app_name}/repo`

2. Add "{app_name}" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        '{app_name}',
    ]

3. Include the {app_name} URLconf in your project urls.py like this::

    path('{app_name}/', include('{app_name}.urls')),

4. Run `python manage.py migrate` to create the {app_name} models.
