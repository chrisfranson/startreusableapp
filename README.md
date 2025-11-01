
startreusableapp
================

Creates a new reusable Django app

Usage
-----------

1. Clone this repo to a location of your choice.

2. cd to a Django project's root directory (where `manage.py` is located).

3. Run `python /path/to/startreusableapp.py [app_name] [app_dir]`.


Arguments
-----------

 - `app_name`: A [valid](https://www.python.org/dev/peps/pep-0008/#package-and-module-names) package/module name
 - `app_dir`: The parent directory in which to put the new application directory structure. The result will look like this:


```
    `app_dir`/
        django-`app_name`/   (or just `app_name` if no prefix)
            Project/
            `app_name`/
                migrations/
                static/
                templates/
                admin.py
                apps.py
                __init__.py
                models.py
                tests.py
                urls.py
                views.py
            docs/
            .git/
            MANIFEST.in
            README.md
            setup.py
            .gitignore
```
