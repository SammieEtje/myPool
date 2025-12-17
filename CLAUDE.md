# Claude Code Guidelines for myPool

## Overview
This is a Django-based F1 betting pool application with a React frontend. The project uses modern Python and JavaScript practices.

## Code Style and Conventions

### Python (Django Backend)
- **Formatting**: Use Black for code formatting
- **Linting**: Use Flake8 with max complexity of 10
- **Imports**: Use isort for import sorting
- **Type Hints**: Add type hints where beneficial
- **Docstrings**: Use Google-style docstrings for functions and classes

### JavaScript/React Frontend
- **Formatting**: Use Prettier
- **Linting**: ESLint with React rules
- **Imports**: Group imports by external libraries, then internal modules
- **Components**: Use functional components with hooks

### Django Specific
- **Models**: Use descriptive field names, add help_text and verbose_name
- **Views**: Use class-based views where appropriate, keep business logic in managers/services
- **URLs**: Use descriptive names for URL patterns
- **Settings**: Keep sensitive data in environment variables
- **Tests**: Write comprehensive unit and integration tests

## Architecture Patterns
- **Separation of Concerns**: Keep business logic separate from views
- **DRY Principle**: Avoid code duplication
- **RESTful APIs**: Follow REST conventions for API endpoints
- **Error Handling**: Use appropriate HTTP status codes and error messages

## Security Considerations
- **Input Validation**: Always validate and sanitize user inputs
- **Authentication**: Use Django's built-in auth system
- **Authorization**: Implement proper permission checks
- **CSRF Protection**: Ensure CSRF tokens are used for forms
- **SQL Injection**: Use Django ORM or parameterized queries

## Performance
- **Database Queries**: Use select_related and prefetch_related for optimization
- **Caching**: Consider caching for frequently accessed data
- **Static Files**: Use Django's static file handling properly
- **Pagination**: Implement pagination for large datasets

## Testing
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test complete workflows
- **Coverage**: Aim for high test coverage (>80%)
- **Fixtures**: Use factory-boy for test data creation

## Git Workflow
- **Branch Naming**: Use descriptive branch names (feature/, bugfix/, hotfix/)
- **Commits**: Write clear, concise commit messages
- **PR Reviews**: All changes require review before merging
- **CI/CD**: All tests must pass before merging

## Deployment
- **Environment Variables**: Use different settings for different environments
- **Database Migrations**: Always create and run migrations
- **Static Files**: Collect and serve static files properly
- **Security**: Use HTTPS in production, set secure headers

## File Structure
```
myPool/
├── betting/          # Main Django app
├── f1betting/        # Django project settings
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
├── requirements.txt  # Python dependencies
└── Dockerfile        # Container configuration
```