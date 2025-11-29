# Testing Guide for F1 Betting Pool

This document provides comprehensive information about testing the F1 Betting Pool application.

## Table of Contents

1. [Overview](#overview)
2. [Test Suite Structure](#test-suite-structure)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Continuous Integration](#continuous-integration)
6. [Code Quality](#code-quality)
7. [Writing New Tests](#writing-new-tests)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The F1 Betting Pool application uses a comprehensive testing strategy that includes:

- **Unit Tests** - Test individual models, methods, and functions
- **Integration Tests** - Test API endpoints and view logic
- **Command Tests** - Test management commands
- **Coverage Reports** - Track code coverage and identify untested code
- **CI/CD Pipeline** - Automated testing on every commit

### Testing Technologies

- **Django Test Framework** - Built-in Django testing
- **pytest** - Modern Python testing framework
- **pytest-django** - Django integration for pytest
- **coverage.py** - Code coverage measurement
- **GitHub Actions** - CI/CD automation

---

## Test Suite Structure

```
betting/tests/
├── __init__.py              # Test package initialization
├── test_models.py           # Model unit tests
├── test_api.py              # API endpoint tests
└── test_commands.py         # Management command tests
```

### Test Coverage by Module

| Module | Test File | Tests | Coverage |
|--------|-----------|-------|----------|
| Models | test_models.py | 40+ tests | Core models |
| API Endpoints | test_api.py | 30+ tests | All viewsets |
| Management Commands | test_commands.py | 15+ tests | seed_data, load_results, score_race |

---

## Running Tests

### Quick Start

Run all tests:
```bash
python manage.py test
```

### Using pytest (Recommended)

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest betting/tests/test_models.py
```

Run specific test class:
```bash
pytest betting/tests/test_models.py::UserProfileModelTest
```

Run specific test method:
```bash
pytest betting/tests/test_models.py::UserProfileModelTest::test_user_profile_creation
```

### Running Tests with Verbosity

Verbose output:
```bash
pytest -v
```

Very verbose output with print statements:
```bash
pytest -vv -s
```

### Filtering Tests

Run only slow tests:
```bash
pytest -m slow
```

Skip slow tests:
```bash
pytest -m "not slow"
```

Run only unit tests:
```bash
pytest -m unit
```

Run only integration tests:
```bash
pytest -m integration
```

---

## Test Coverage

### Generate Coverage Report

Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

Or with pytest:
```bash
pytest --cov=betting --cov-report=term-missing
```

### HTML Coverage Report

Generate detailed HTML report:
```bash
coverage run --source='.' manage.py test
coverage html
```

Open the report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

### Coverage Goals

- **Overall Coverage**: Target 80%+
- **Models**: Target 90%+
- **Views/API**: Target 85%+
- **Management Commands**: Target 75%+

---

## Continuous Integration

### GitHub Actions Workflow

The project uses GitHub Actions for automated testing on every push and pull request.

**Workflow File**: `.github/workflows/ci.yml`

### CI Pipeline Jobs

1. **Test Suite** (Python 3.11 & 3.12)
   - Runs all tests
   - Generates coverage reports
   - Uploads coverage to Codecov

2. **Code Quality**
   - Linting with flake8
   - Code formatting check with black
   - Import sorting check with isort

3. **Security Scan**
   - Dependency vulnerability scanning with safety
   - Code security scanning with bandit

4. **Build Check**
   - Verifies migrations work
   - Collects static files
   - Runs deployment checks

5. **Integration Tests**
   - Seeds database
   - Loads race results
   - Scores races
   - Verifies data integrity

6. **Performance Tests**
   - Checks database query performance
   - Identifies N+1 queries

### Viewing CI Results

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select a workflow run to see results
4. Each job shows detailed logs and test output

### CI Status Badge

Add this to your README.md:
```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/F1%20Betting%20Pool%20CI%2FCD/badge.svg)
```

---

## Code Quality

### Linting with flake8

Check code style:
```bash
flake8 .
```

Check specific file:
```bash
flake8 betting/models.py
```

### Code Formatting with black

Check if code needs formatting:
```bash
black --check .
```

Auto-format code:
```bash
black .
```

Format specific file:
```bash
black betting/models.py
```

### Import Sorting with isort

Check import ordering:
```bash
isort --check-only .
```

Auto-sort imports:
```bash
isort .
```

### Security Scanning

Check for known vulnerabilities:
```bash
safety check
```

Run security linter:
```bash
bandit -r betting/
```

### Running All Quality Checks

```bash
# Linting
flake8 .

# Formatting
black --check .

# Import sorting
isort --check-only .

# Security
safety check
bandit -r betting/
```

---

## Writing New Tests

### Test Structure

Follow this pattern for new tests:

```python
from django.test import TestCase
from betting.models import YourModel

class YourModelTest(TestCase):
    """Test YourModel"""

    def setUp(self):
        """Set up test dependencies"""
        # Create test data
        pass

    def test_something_specific(self):
        """Test a specific behavior"""
        # Arrange
        expected = "expected value"

        # Act
        result = some_function()

        # Assert
        self.assertEqual(result, expected)

    def tearDown(self):
        """Clean up after tests (optional)"""
        pass
```

### Model Tests

Test checklist for models:
- ✅ Model creation
- ✅ String representation (`__str__`)
- ✅ Model properties and methods
- ✅ Model relationships
- ✅ Model validation
- ✅ Model signals

Example:
```python
def test_driver_full_name_property(self):
    """Test full_name property"""
    driver = Driver.objects.create(
        first_name='Lewis',
        last_name='Hamilton',
        driver_number=44,
        team='Mercedes'
    )
    self.assertEqual(driver.full_name, 'Lewis Hamilton')
```

### API Tests

Test checklist for API endpoints:
- ✅ List endpoint (GET)
- ✅ Detail endpoint (GET)
- ✅ Create endpoint (POST)
- ✅ Update endpoint (PUT/PATCH)
- ✅ Delete endpoint (DELETE)
- ✅ Authentication/permissions
- ✅ Filtering and searching
- ✅ Validation errors

Example:
```python
def test_create_bet_authenticated(self):
    """Test creating a bet while authenticated"""
    self.client.force_authenticate(user=self.user)
    data = {
        'race': self.race.id,
        'driver': self.driver.id,
        'predicted_position': 1
    }
    response = self.client.post('/api/bets/', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### Command Tests

Test checklist for management commands:
- ✅ Command runs successfully
- ✅ Command creates expected data
- ✅ Command handles errors gracefully
- ✅ Command options work correctly
- ✅ Command output is correct

Example:
```python
def test_seed_data_creates_drivers(self):
    """Test seed_data creates drivers"""
    out = StringIO()
    call_command('seed_data', stdout=out)

    drivers = Driver.objects.all()
    self.assertGreaterEqual(drivers.count(), 20)
```

### Best Practices

1. **One test, one assertion** - Keep tests focused
2. **Descriptive names** - Test names should describe what they test
3. **AAA Pattern** - Arrange, Act, Assert
4. **Use setUp and tearDown** - Share test data setup
5. **Test edge cases** - Don't just test the happy path
6. **Mock external services** - Don't rely on external APIs in tests
7. **Keep tests fast** - Fast tests run more often

---

## Troubleshooting

### Common Issues

#### Issue: Tests fail with database errors

**Solution**: Make sure migrations are applied
```bash
python manage.py migrate
```

#### Issue: Import errors in tests

**Solution**: Make sure you're in the project root directory and the app is in INSTALLED_APPS

#### Issue: Coverage report is empty

**Solution**: Make sure you're running coverage with the correct source
```bash
coverage run --source='betting' manage.py test
```

#### Issue: Tests pass locally but fail in CI

**Solution**: Check environment variables and dependencies
- Verify .env file is created in CI
- Check Python version matches
- Verify all dependencies are installed

#### Issue: Slow test execution

**Solution**: Use pytest-xdist for parallel execution
```bash
pip install pytest-xdist
pytest -n auto  # Use all CPU cores
```

### Debugging Tests

Add print statements:
```bash
pytest -s  # Don't capture output
```

Use debugger:
```python
import ipdb; ipdb.set_trace()  # Add breakpoint
```

Run single failing test:
```bash
pytest betting/tests/test_models.py::TestClass::test_method -vv
```

### Test Database

By default, Django creates a test database for each test run. You can:

Keep test database:
```bash
python manage.py test --keepdb
```

This speeds up subsequent test runs.

---

## Quick Reference

### Common Commands

```bash
# Run all tests
python manage.py test

# Run with pytest
pytest

# Run with coverage
pytest --cov=betting --cov-report=html

# Run specific test file
pytest betting/tests/test_models.py

# Run linting
flake8 .

# Format code
black .

# Sort imports
isort .

# Security check
safety check

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Test Markers

```python
@pytest.mark.slow
def test_something_slow():
    pass

@pytest.mark.integration
def test_api_integration():
    pass

@pytest.mark.unit
def test_model_method():
    pass
```

Run specific marker:
```bash
pytest -m slow
pytest -m "not slow"
pytest -m integration
```

---

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [Real Python Testing Guide](https://realpython.com/testing-in-django/)

---

**Happy Testing! 🏎️🧪**
