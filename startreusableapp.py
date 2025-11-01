import sys
import os
import errno
import argparse
import subprocess
import fileinput
from string import Template


description = 'This creates a reusable Django app'

# Parse script arguments
parser = argparse.ArgumentParser(description=description)
parser.add_argument('app_name', help='Name of the Django app to create')
parser.add_argument('parent_dir', help='Parent directory where the app will be created')
parser.add_argument('--no-input', dest='no_input', default=False, action='store_true',
                    help='Run without interactive prompts (use with other flags to specify options)')
parser.add_argument('--no-color', dest='no_color', default=False, action='store_true',
                    help='Disable colored output')
parser.add_argument('--prefix', dest='add_prefix', default=False, action='store_true',
                    help='Prefix package name with "django-"')
parser.add_argument('--editor', dest='editor', default='nano',
                    help='Editor to use for file editing (default: nano)')
parser.add_argument('--with-bootstrap', dest='with_bootstrap', default=None, action='store_true',
                    help='Include Bootstrap, django-compressor, and django-bootstrap5')
parser.add_argument('--no-bootstrap', dest='with_bootstrap', action='store_false',
                    help='Skip Bootstrap setup')
parser.add_argument('--with-drf', dest='with_drf', default=None, action='store_true',
                    help='Include Django REST Framework scaffold')
parser.add_argument('--no-drf', dest='with_drf', action='store_false',
                    help='Skip DRF setup')
parser.add_argument('--with-oauth', dest='with_oauth', default=None, action='store_true',
                    help='Include OAuth2 authentication setup (requires --with-drf)')
parser.add_argument('--no-oauth', dest='with_oauth', action='store_false',
                    help='Skip OAuth setup')
parser.add_argument('--with-views', dest='with_views', default=None, action='store_true',
                    help='Add templates, static, and IndexView scaffold')
parser.add_argument('--no-views', dest='with_views', action='store_false',
                    help='Skip view scaffold')
parser.add_argument('--install', dest='install_now', default=None, action='store_true',
                    help='Install with pip immediately after creation')
parser.add_argument('--no-install', dest='install_now', action='store_false',
                    help='Skip pip installation')
args = parser.parse_args()

# Important directories
this_script_dir = os.path.dirname(os.path.realpath(__file__))
initial_cwd = os.getcwd()
repo_dir = ''
parent_dir = ''
project_dir = ''
templates_dir = ''
static_dir = ''

# More user config
editor = 'nano'
package_prefix = ''

# Fancy text
fancy_text = {
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'b': '\033[1m',
    'end': '\033[0m',
}
if args.no_color:
    fancy_text = { key:'' for (key, value) in fancy_text.items() }


def main():
    global editor, package_prefix
    if not os.path.isfile('manage.py'):
        print("{red}Run this baby from a Django project's root directory.{end}".format(**fancy_text))
        sys.exit()

    # Set editor from args or ask user
    if args.editor != 'nano':
        editor = args.editor
    elif not args.no_input:
        user_input = input("{purple}What command should we use to edit files?{end} [nano] ".format(**fancy_text))
        if user_input != '':
            editor = user_input

    # Set package prefix from args or ask user
    if args.add_prefix:
        package_prefix = 'django-'
    elif user_yesno("Prefix the new package name with \"django-\"?", default='n'):
        package_prefix = 'django-'

    module_name = args.app_name.replace('-', '_')
    package_dirname = package_prefix + args.app_name
    repo_dir = os.path.join(args.parent_dir, package_dirname)
    app_root_dir = os.path.join(repo_dir, module_name)
    project_dir = os.path.join(repo_dir, "Project")

    print("\n\n\n\n{b}{yellow}ANNNNNNND AWAY!!{end}\n\n\n\n".format(**fancy_text))

    startapp_command = f'python manage.py startapp {module_name} {app_root_dir}'
    if not os.path.isdir(app_root_dir):
        try:
            print_cyan(f"mkdir -p {repo_dir}")
            mkdir_p(app_root_dir)
        except OSError:
            print("{red}Couldn't create directory: {repo_dir}{end}".format(repo_dir=repo_dir, **fancy_text))
            sys.exit()
        try:
            print_cyan("mkdir {}".format(project_dir))
            os.mkdir(project_dir)
        except OSError:
            print("{red}Couldn't create directory: {project_dir}{end}".format(project_dir=project_dir, **fancy_text))
            sys.exit()

    call(startapp_command)

    print_cyan(f'cd {repo_dir}')
    os.chdir(repo_dir)

    copy_template_file('.gitignore')
    call('git init && git add .')
    call("git commit -m 'Initial commit!\n\nCreate an app scaffold with \"python manage.py startapp\"'")
    call('git checkout -b dev')

    mkdirs(['docs'])
    call('touch docs/.gitignore')

    template_files = [
        'README.md',
        'setup.py',
        'MANIFEST.in',
    ]
    for file in template_files:
        copy_template_file(file)

    if user_yesno("Commit now, with message: 'Package the app for reusability'?"):
        call("git add . && git commit -m 'Package the app for reusability'")

    # Determine if we should add views/templates/static
    add_views = args.with_views if args.with_views is not None else user_yesno("Add templates/, static/, and urls.py?")

    if add_views:
        templates_dir = os.path.join(module_name, 'templates', module_name)
        static_dir = os.path.join(module_name, 'static', module_name)
        mkdirs([templates_dir, static_dir])
        copy_template_file('urls.py', module_name)

    if add_views and templates_dir and user_yesno("Add a scaffold IndexView, template, and entry in `urls.py`?"):
        copy_template_file(
            'views.py',
            destination_subdirectory=module_name
        )
        copy_template_file(
            'urls-with-view.py',
            destination_subdirectory=module_name,
            destination_filename='urls.py'
        )

        # Determine if we should add Bootstrap
        add_bootstrap = args.with_bootstrap if args.with_bootstrap is not None else user_yesno(f"""How 'bout all this?

 - Get the latest Bootstrap (bundle)
 - require django-compressor
 - require django-bootstrap5
 - add templates/{module_name}/base.html
 - add static/css/{module_name}.css
 - add static/js/{module_name}.js

 """)

        if templates_dir and static_dir and add_bootstrap:
            css_dir = os.path.join(static_dir, 'css')
            js_dir = os.path.join(static_dir, 'js')
            call(f"wget https://raw.githubusercontent.com/twbs/bootstrap/main/dist/css/bootstrap.css -P {css_dir}")
            call(f"wget https://raw.githubusercontent.com/twbs/bootstrap/main/dist/js/bootstrap.bundle.js -P {js_dir}")
            install_requires = ['django-compressor', 'django-bootstrap5']
            install_requires_string = ''
            for package in install_requires:
                install_requires_string += f"        '{package}',\n"
            install_requires_string = install_requires_string.rstrip()
            copy_template_file(
                'index-bootstrap.html',
                destination_subdirectory=templates_dir,
                destination_filename='index.html',
            )
            copy_template_file(
                'base.html',
                destination_subdirectory=templates_dir,
            )
            copy_template_file(
                'setup-with-requirements.py',
                substitutions={'install_requires': install_requires_string},
                destination_filename='setup.py',
            )
            copy_template_file(
                'app_name.css',
                destination_subdirectory=css_dir,
                destination_filename=f'{module_name}.css'
            )
            copy_template_file(
                'app_name.js',
                destination_subdirectory=js_dir,
                destination_filename=f'{module_name}.js'
            )
        else:
            copy_template_file(
                'index-barebones.html',
                destination_subdirectory=templates_dir,
                destination_filename='index.html'
            )

    # Optionally add DRF scaffold
    add_drf = args.with_drf if args.with_drf is not None else user_yesno("Would you like to include Django REST Framework (DRF) support?")

    if add_drf:
        # Check if we should add OAuth support
        add_oauth = args.with_oauth if args.with_oauth is not None else user_yesno("Include OAuth2 authentication setup with user-scoped models?")

        if add_oauth:
            # OAuth-ready templates (includes models, serializers, views with user scoping)
            copy_template_file('models_oauth.py', destination_subdirectory=module_name, destination_filename='models.py')
            copy_template_file('serializers_oauth.py', destination_subdirectory=module_name, destination_filename='serializers.py')
            copy_template_file('api_views_oauth.py', destination_subdirectory=module_name, destination_filename='api_views.py')
            copy_template_file('urls-with-oauth.py', destination_subdirectory=module_name, destination_filename='urls.py')
            update_setup_py_for_oauth()
        else:
            # Standard DRF templates
            copy_template_file('serializers.py', destination_subdirectory=module_name)
            copy_template_file('api_views.py', destination_subdirectory=module_name)
            copy_template_file('urls-with-drf.py', destination_subdirectory=module_name, destination_filename='urls.py')
            update_setup_py_for_drf()

    # Bring the user back to where we started
    print_cyan(f'cd {initial_cwd}')
    os.chdir(initial_cwd)

    # Determine if we should install now
    install = args.install_now if args.install_now is not None else user_yesno(f"Install {module_name} with pip now?")

    if install:
        call(f'pip install -e {repo_dir}')
    else:
        print("You can install it later with:")
        print(f'pip install -e {repo_dir}')

    print('\n{yellow}{b}**** DUNZO! :D ****{end}\n'.format(**fancy_text))

    if user_yesno("Display the README now?"):
        readme_file = os.path.join(repo_dir, "README.md")
        call(f"cat {readme_file}")
        print("\n\n")


def mkdirs(directories):
    for directory in directories:
        print_cyan(f'mkdir -p {directory}')
        mkdir_p(directory)


def copy_template_file(filename, destination_subdirectory='', substitutions=None, destination_filename=False, ask_to_edit=False):
    global editor, package_prefix
    template_file = os.path.join(this_script_dir, "template_files", filename)
    if not destination_filename:
        destination_filename = filename
    destination_file = os.path.join(repo_dir, destination_subdirectory, destination_filename)
    print_cyan(f'Creating {destination_filename}')
    # Open the template version
    with open(template_file, 'r') as file:
        filedata = file.read()
    # Replace the template variables
    filedata = Template(filedata)
    _substitutions = {
        'app_name': args.app_name,
        'app_name_capitalized': args.app_name.capitalize(),
        'app_name_lowercase': args.app_name.lower(),
        'package_prefix': package_prefix,
        'app_header_line': '='*len(args.app_name),
    }
    if substitutions:
        _substitutions |= substitutions
    filedata = filedata.substitute(**_substitutions)
    # Write the modified version to the new app's dir
    with open(destination_file, 'w') as file:
        file.write(filedata)
    if ask_to_edit and user_yesno(f"Edit {filename} with {editor} now?"):
        call(f'{editor} {destination_file}')


def update_setup_py_for_drf():
    """Update setup.py to include DRF and drf-spectacular as requirements."""
    setup_file = os.path.join(repo_dir, 'setup.py')
    with open(setup_file, 'r') as file:
        content = file.read()

    install_requires_str = "        'djangorestframework',\n        'drf-spectacular',"

    if "install_requires" in content:
        content = content.replace("install_requires=[", f"install_requires=[\n{install_requires_str}")
    else:
        content = content.replace("setup(", f"setup(\n    install_requires=[\n{install_requires_str}\n    ],")

    with open(setup_file, 'w') as file:
        file.write(content)


def update_setup_py_for_oauth():
    """Update setup.py to include DRF, drf-spectacular, and django-oauth-toolkit."""
    setup_file = os.path.join(repo_dir, 'setup.py')
    with open(setup_file, 'r') as file:
        content = file.read()

    install_requires_str = "        'djangorestframework',\n        'drf-spectacular',\n        'django-oauth-toolkit',"

    if "install_requires" in content:
        content = content.replace("install_requires=[", f"install_requires=[\n{install_requires_str}")
    else:
        content = content.replace("setup(", f"setup(\n    install_requires=[\n{install_requires_str}\n    ],")

    with open(setup_file, 'w') as file:
        file.write(content)


def user_yesno(question, default='y'):
    if args.no_input:
        user_input = default
    else:
        user_input = input("\n{purple}{question}{end} [y]/n ".format(question=question, **fancy_text))
    return user_input.lower() == 'y' or user_input.lower() == 'yes' or user_input == ''


def call(command, print_it=True):
    if print_it:
        print("\n{cyan}{command}{end}".format(command=command, **fancy_text))
    os.system(command)


def print_cyan(s):
    print("\n{cyan}{s}{end}".format(s=s, **fancy_text))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

main()
