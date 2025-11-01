# startreusableapp

A powerful scaffolding tool for creating production-ready Django reusable apps with modern best practices.

## Features

- 🎯 **Modern Django 5.x patterns** with type hints
- 🔐 **OAuth2 authentication** ready (django-oauth-toolkit)
- 🧪 **Pytest testing** with comprehensive test coverage
- 🎨 **Pre-commit hooks** for code quality (black, isort, flake8, mypy)
- 🚀 **GitHub Actions CI/CD** workflow
- 📦 **Management commands** scaffold
- 🔌 **Django REST Framework** integration with ViewSets
- 🎭 **User-scoped models** for multi-tenant applications
- 📝 **pyproject.toml** for modern Python packaging
- ⚙️ **Fully customizable** with command-line arguments

## Installation

```bash
git clone https://github.com/chrisfranson/startreusableapp.git
cd startreusableapp
```

Or use the alias:
```bash
alias startreusableapp="python /path/to/startreusableapp/startreusableapp.py"
```

## Quick Start

### Interactive Mode

```bash
cd your-django-project/
startreusableapp myapp /path/to/apps
```

The script will prompt you for options.

### Non-Interactive Mode (Fully Automated)

```bash
cd your-django-project/
startreusableapp myapp /path/to/apps \
  --no-input \
  --prefix \
  --with-drf \
  --with-oauth \
  --with-tests \
  --with-precommit \
  --with-ci \
  --with-management-commands \
  --install
```

This creates a complete, production-ready app with all features enabled!

## Command-Line Options

### Basic Options

| Option | Description |
|--------|-------------|
| `app_name` | Name of the Django app to create (required) |
| `parent_dir` | Parent directory for the app (required) |
| `--no-input` | Run without interactive prompts |
| `--no-color` | Disable colored output |
| `--prefix` | Prefix package name with "django-" |
| `--editor EDITOR` | Editor to use (default: nano) |

### Feature Flags

| Option | Description |
|--------|-------------|
| `--with-drf` / `--no-drf` | Include Django REST Framework scaffold |
| `--with-oauth` / `--no-oauth` | Include OAuth2 authentication (requires --with-drf) |
| `--with-tests` / `--no-tests` | Include pytest testing scaffold |
| `--with-precommit` / `--no-precommit` | Include pre-commit hooks and pyproject.toml |
| `--with-ci` / `--no-ci` | Include GitHub Actions CI/CD workflow |
| `--with-management-commands` / `--no-management-commands` | Include management commands scaffold |
| `--with-views` / `--no-views` | Add templates, static, and IndexView |
| `--with-bootstrap` / `--no-bootstrap` | Include Bootstrap setup (with views) |
| `--install` / `--no-install` | Install with pip immediately |

## Directory Structure

```
parent_dir/
  django-myapp/          # Git repository root
    myapp/               # Django module
      migrations/
      management/
        commands/
          example_command.py
      static/myapp/
      templates/myapp/
      api_views.py       # With --with-drf
      models.py          # With --with-oauth (user-scoped)
      serializers.py
      urls.py
      views.py
      admin.py
      apps.py
      __init__.py
    tests/
      conftest.py
      settings.py
      test_models.py
      test_api.py
    .github/
      workflows/
        ci.yml
    Project/             # IDE project files
    docs/
    .git/
    .gitignore
    .pre-commit-config.yaml
    pyproject.toml
    pytest.ini
    MANIFEST.in
    README.md
    setup.py
```

## OAuth2 Integration

With `--with-oauth`, the app is configured for multi-tenant, user-scoped data:

### Models
```python
class ExampleModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Views
```python
class ExampleModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExampleModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

Users can only access their own data automatically!

## Testing

With `--with-tests`:

```bash
# Install test dependencies
pip install -e .[test]

# Run tests
pytest

# With coverage
pytest --cov=myapp
```

Tests include:
- Model creation and validation
- User scoping and isolation
- API authentication
- CRUD operations
- Cascade deletion

## Code Quality

With `--with-precommit`:

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Includes:
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **Django checks**: System validation

## CI/CD

With `--with-ci`, get GitHub Actions workflows that:

- Test across Python 3.11, 3.12
- Test across Django 5.0, 5.1
- Run pre-commit hooks
- Generate coverage reports
- Security scanning
- Automatic on push/PR

## Management Commands

With `--with-management-commands`:

```bash
python manage.py example_command --example-arg test --verbose
```

Includes modern patterns:
- Type hints
- Argument parsing
- Styled output
- Verbose mode

## Use Cases

### OAuth Playground Apps

Perfect for creating experimental apps that integrate with OAuth projects:

```bash
startreusableapp ele /storage/Projects/webapps/IOLabs/AI/Ele \
  --no-input \
  --with-drf \
  --with-oauth \
  --with-tests \
  --install
```

Then add to your OAuth project's `INSTALLED_APPS` and users get isolated data automatically!

### Production Libraries

Create production-ready packages:

```bash
startreusableapp notifications /path/to/libs \
  --no-input \
  --prefix \
  --with-drf \
  --with-tests \
  --with-precommit \
  --with-ci
```

### Learning Projects

Start simple and add features incrementally:

```bash
# Start minimal
startreusableapp blog /tmp/learning \
  --no-input \
  --no-drf \
  --no-oauth

# Add features later as you learn!
```

## Requirements

- Python 3.11+
- Django 5.0+
- A Django project (must run from project root with manage.py)

## Contributing

Pull requests welcome! For major changes, please open an issue first.

## License

MIT

## Credits

Created by Chris Franson
