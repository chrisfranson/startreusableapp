import sys, os 
import errno, argparse, subprocess, fileinput

description = 'This creates a reusable Django app'

# Parse script arguments
parser = argparse.ArgumentParser(description=description)
parser.add_argument('app_name')
parser.add_argument('app_dir')
args = parser.parse_args()

# Important directories
this_script_dir = os.path.dirname(os.path.realpath(__file__))
initial_cwd = os.getcwd()
repo_dir = ''
app_dir = ''
project_dir = ''

# More user config
editor = 'nano'
package_prefix = ''


def main():
	global editor, package_prefix
	if not os.path.isfile('manage.py'):
		print("Run this baby from a Django project's root directory.")
		sys.exit()

	user_input = input("What command should we use to edit files? [nano] ")
	if user_input != '':
		editor = user_input

	if user_yesno("Prefix the new package name with \"django-\"?"):
		package_prefix = 'django-'

	package_dir = package_prefix + args.app_name
	repo_dir = os.path.join(args.app_dir, args.app_name, package_dir)
	app_dir = os.path.join(repo_dir, args.app_name)
	project_dir = os.path.join(args.app_dir, args.app_name, "Project")

	print("\n\n\n\nANNNNNNND AWAY!!\n\n\n\n")

	startapp_command = 'python manage.py startapp {} {}'.format(args.app_name, app_dir)
	if not os.path.isdir(app_dir):
		try:
			print("mkdir -p {}".format(repo_dir))
			mkdir_p(app_dir)
		except OSError:
			print("Couldn't create directory: {}".format(repo_dir))
			sys.exit()
		try:
			print("mkdir {}".format(project_dir))
			os.mkdir(project_dir)
		except OSError:
			print("Couldn't create directory: {}".format(project_dir))
			sys.exit()

	call(startapp_command)

	print('cd {}'.format(repo_dir))
	os.chdir(repo_dir)

	copy_template_file('.gitignore', '', False)
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
		dirs = [
			'{0}/templates/{0}'.format(args.app_name),
			'{0}/static/{0}'.format(args.app_name),
		]
		mkdirs(dirs)
		copy_template_file('urls.py', args.app_name)

	# Bring the user back to where we started
	print('cd {}'.format(initial_cwd))
	os.chdir(initial_cwd)

	if user_yesno("Install {} with pip now?".format(args.app_name)):
		call('pip install -e {}'.format(repo_dir))

	print('\n**** DUNZO! :D ****\n')

	if user_yesno("Display the README now?"):
		readme_file = os.path.join(repo_dir, "README.md")
		call("cat {}".format(readme_file))
		print("\n\n")


def mkdirs(directories):
	for directory in directories:
		print('mkdir -p {}'.format(directory))
		mkdir_p(directory)


def copy_template_file(filename, destination_subdirectory='', ask_to_edit=True):
	global editor, package_prefix
	template_file = os.path.join(this_script_dir, "template_files", filename)
	destination_file = os.path.join(repo_dir, destination_subdirectory, filename)
	print('Creating {}'.format(destination_file))
	# Open the template version
	with open(template_file, 'r') as file:
		filedata = file.read()
	# Replace the {app_name} and {app_header_line} variables
	filedata = filedata.format(
		app_name=args.app_name,
		package_prefix=package_prefix,
		app_header_line='='*len(args.app_name)
	)
	# Write the modified version to the new app's dir
	with open(destination_file, 'w') as file:
		file.write(filedata)
	if ask_to_edit and user_yesno("Edit {} with {} now?".format(filename, editor)):
		call('{} {}'.format(editor, destination_file))


def user_yesno(question):
	user_input = input(question + ' [y]/n ')
	return user_input.lower() == 'y' or user_input.lower() == 'yes' or user_input == ''


def call(command, print_it=True):
	if print_it:
		print(command)
	os.system(command)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

main()
