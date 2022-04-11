import sys, os 
import errno, argparse, subprocess, fileinput
from string import Template

description = 'This creates a reusable Django app'

# Parse script arguments
parser = argparse.ArgumentParser(description=description)
parser.add_argument('app_name')
parser.add_argument('parent_dir')
parser.add_argument('--no-color', dest='no_color', default=False, action='store_true')
args = parser.parse_args()

# Important directories
this_script_dir = os.path.dirname(os.path.realpath(__file__))
initial_cwd = os.getcwd()
repo_dir = ''
parent_dir = ''
project_dir = ''

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
		print("{red}Run this baby from a Django project's root directory.{end}")
		sys.exit()

	user_input = input("{purple}What command should we use to edit files?{end} [nano] ".format(**fancy_text))
	if user_input != '':
		editor = user_input

	if user_yesno("Prefix the new package name with \"django-\"?"):
		package_prefix = 'django-'

	package_dir = package_prefix + args.app_name
	repo_dir = os.path.join(args.parent_dir, args.app_name, package_dir)
	parent_dir = os.path.join(repo_dir, args.app_name)
	project_dir = os.path.join(args.parent_dir, args.app_name, "Project")

	print("\n\n\n\n{b}{yellow}ANNNNNNND AWAY!!{end}\n\n\n\n".format(**fancy_text))

	startapp_command = f'python manage.py startapp {args.app_name} {parent_dir}'
	if not os.path.isdir(parent_dir):
		try:
			print_cyan(f"mkdir -p {repo_dir}")
			mkdir_p(parent_dir)
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

	if user_yesno("Add templates/, static/, and urls.py?"):
		templates_dir = os.path.join(args.app_name, 'templates', args.app_name)
		static_dir = os.path.join(args.app_name, 'static', args.app_name)
		mkdirs([templates_dir, static_dir])
		copy_template_file('urls.py', args.app_name)

	if user_yesno("Add a scaffold IndexView, template, and entry in `urls.py`?"):
		copy_template_file(
			'views.py',
			destination_subdirectory=args.app_name
		)
		copy_template_file(
			'urls-with-view.py',
			destination_subdirectory=args.app_name,
			destination_filename='urls.py'
		)
		copy_template_file(
			'index.html',
			destination_subdirectory='{}/templates/{}'.format(args.app_name, args.app_name)
		)

	# Bring the user back to where we started
	print_cyan(f'cd {initial_cwd}')
	os.chdir(initial_cwd)

	if user_yesno(f"Install {args.app_name} with pip now?"):
		call(f'pip install -e {repo_dir}')

	print('\n{yellow}{b}**** DUNZO! :D ****{end}\n'.format(**fancy_text))

	if user_yesno("Display the README now?"):
		readme_file = os.path.join(repo_dir, "README.md")
		call(f"cat {readme_file}")
		print("\n\n")


def mkdirs(directories):
	for directory in directories:
		print_cyan(f'mkdir -p {directory}')
		mkdir_p(directory)


def copy_template_file(filename, destination_subdirectory='', destination_filename=False, ask_to_edit=False):
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
	filedata = filedata.substitute(
		app_name=args.app_name,
		package_prefix=package_prefix,
		app_header_line='='*len(args.app_name)
	)
	# Write the modified version to the new app's dir
	with open(destination_file, 'w') as file:
		file.write(filedata)
	if ask_to_edit and user_yesno(f"Edit {filename} with {editor} now?"):
		call(f'{editor} {destination_file}')


def user_yesno(question):
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
