# F1 Betting Pool 🏎️

A modern, responsive web application for Formula 1 betting pools among friends. Built with Django, Django REST Framework, and vanilla JavaScript.

## Build Status

[![CI/CD Pipeline](https://github.com/SammieEtje/myPool/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SammieEtje/myPool/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/SammieEtje/myPool/branch/main/graph/badge.svg)](https://codecov.io/gh/SammieEtje/myPool)
[![Python 3.11 | 3.12 | 3.14](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django 5.1](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![F1](https://img.shields.io/badge/Racing-F1-DC0000)](https://www.formula1.com/)

## Features

### Core Functionality
- **User Authentication** - Social login (Google, GitHub) with optional Multi-Factor Authentication (MFA)
- **Competition Management** - Administrators can create and manage F1 seasons/championships
- **Race Betting** - Users predict Top 10 finishing positions for each race
- **Deadline Management** - Betting automatically closes at race start time
- **Points System** - Configurable scoring for exact position matches and correct driver predictions
- **Live Leaderboard** - Real-time rankings and competition standings
- **Race Results** - View historical race results and your prediction accuracy
- **Responsive Design** - Mobile-first, racing-inspired UI with dark theme

### Admin Features
- **Statistics Dashboard** - Real-time overview of users, races, bets, and more on admin homepage
- **Competition Management** - Create and manage F1 seasons/championships
- **Race Management** - Add races, set betting deadlines, manage race results
- **Driver Management** - Track current and historical F1 drivers
- **User Management** - Manage users, permissions, and profiles
- **Scoring System** - Automated race scoring with management commands
- **Detailed Tutorial** - Step-by-step [Admin Tutorial](ADMIN_TUTORIAL.md) for all tasks

### Technical Features
- RESTful API with Django REST Framework
- Single Page Application (SPA) architecture
- Responsive, mobile-first design
- Racing-inspired color scheme (Red, Electric Blue, Gold)
- Extensible bet types system (ready for future bet types)
- OpenF1 API integration with manual entry fallback
- Azure-ready deployment configuration

## Quick Start

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd myPool
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Seed the database with sample data**
```bash
python manage.py seed_data
```

This will create:
- Admin user: `admin@f1betting.com` / `admin123`
- 5 test users: `user1@test.com` to `user5@test.com` / `test123`
- 20 F1 drivers (2024 grid)
- 2025 F1 Championship with 24 races
- Default bet types

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Frontend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API: http://localhost:8000/api/

## Development vs Production Mode

### Local Development Mode (Your Laptop)

**The application is already configured for easy local development without HTTPS!**

When running on your laptop, the system automatically disables all HTTPS requirements when `DEBUG=True`. This means you can run the application on `http://localhost:8000` without any SSL certificates or HTTPS setup.

**Quick Setup for Local Development:**

```bash
# 1. Use the development environment configuration
cp .env.development .env

# 2. Run migrations
python manage.py migrate

# 3. Create a superuser (optional)
python manage.py createsuperuser

# 4. Start the development server
python manage.py runserver

# 5. Access at http://localhost:8000 (no HTTPS required!)
```

**What happens in development mode (`DEBUG=True`):**
- ✅ No HTTPS/SSL required - works on `http://localhost:8000`
- ✅ Detailed error pages for easier debugging
- ✅ Cookies work over HTTP
- ✅ Email backend prints to console (no SMTP setup needed)
- ✅ SQLite database (no database server required)
- ✅ Static files served by Django (no CDN needed)

**Environment variables for development:**
- `DEBUG=True` - Enables development mode
- `SECRET_KEY` - Uses default insecure key (fine for local dev)
- `ALLOWED_HOSTS=localhost,127.0.0.1` - Allows local access
- `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` - Prints emails to console

See `.env.development` for a complete development configuration with detailed comments.

### Production Mode (Azure, Heroku, etc.)

For production deployments, you **must** set `DEBUG=False`, which automatically enables all security features:

**What happens in production mode (`DEBUG=False`):**
- 🔒 HTTPS/SSL required - HTTP requests redirect to HTTPS
- 🔒 HSTS enabled - Browser enforces HTTPS for 1 year
- 🔒 Secure cookies - Session/CSRF cookies only sent over HTTPS
- 🔒 Security headers - XSS protection, clickjacking prevention
- 🔒 Strong secret key required
- 🔒 Proper email backend needed for MFA

**Production setup requirements:**
1. Set `DEBUG=False` in environment variables
2. Use a strong, random `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up HTTPS/SSL certificates (handled by Azure/Heroku)
5. Use production database (PostgreSQL, Azure SQL)
6. Configure email backend for MFA (Gmail SMTP, SendGrid, etc.)

See the [Deployment](#deployment) section below for detailed production setup instructions.

## Documentation

### For Administrators
📚 **[Admin Tutorial](ADMIN_TUTORIAL.md)** - Comprehensive step-by-step guide for managing the F1 betting pool:
- Setting up competitions and races
- Managing drivers and users
- Loading race results
- Scoring races and viewing standings
- Troubleshooting common issues
- Best practices for running a season

### For Developers
- **[Quick Start Guide](QUICKSTART.md)** - Fast setup instructions for development
- **[Testing Guide](TESTING.md)** - Comprehensive testing documentation and CI/CD information
- **README.md** (this file) - Project overview and technical documentation

## Project Structure

```
myPool/
├── f1betting/              # Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── betting/               # Main betting app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── admin.py           # Admin configuration with statistics dashboard
│   ├── signals.py         # User profile signals
│   ├── f1_api.py          # F1 API integration
│   └── management/        # Management commands
│       └── commands/
│           ├── seed_data.py      # Database seeding
│           ├── load_results.py   # Load race results
│           └── score_race.py     # Bet scoring
├── templates/             # HTML templates
│   ├── account/           # Authentication pages
│   ├── admin/             # Admin customizations
│   └── index.html         # SPA main template
├── static/                # Static assets
│   ├── css/
│   │   ├── design-system.css  # Design system
│   │   └── main.css           # Main styles
│   └── js/
│       └── app.js         # Frontend JavaScript
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── azure-deploy.yml      # Azure deployment config
├── startup.sh            # Azure startup script
├── README.md             # This file
├── ADMIN_TUTORIAL.md     # Step-by-step admin guide
└── QUICKSTART.md         # Quick setup guide
```

## Database Models

### Core Models
- **UserProfile** - Extended user information with betting statistics
- **Competition** - F1 season/championship
- **Race** - Individual F1 race with betting deadline
- **Driver** - F1 driver information
- **BetType** - Extensible bet type definitions
- **Bet** - User predictions for races
- **RaceResult** - Actual race results
- **CompetitionStanding** - Leaderboard rankings

## API Endpoints

### Competitions
- `GET /api/competitions/` - List all published competitions
- `GET /api/competitions/{id}/` - Competition details
- `GET /api/competitions/{id}/races/` - Races in competition
- `GET /api/competitions/{id}/standings/` - Leaderboard
- `POST /api/competitions/{id}/join/` - Join competition

### Races
- `GET /api/races/` - List races (filter by competition, status, upcoming)
- `GET /api/races/{id}/` - Race details with results and user bets
- `GET /api/races/{id}/results/` - Race results
- `GET /api/races/{id}/my_bet/` - Current user's bet

### Bets
- `GET /api/bets/` - User's bets
- `POST /api/bets/` - Create single bet
- `POST /api/bets/bulk_create/` - Create multiple bets (Top 10)
- `GET /api/bets/my_bets/` - All user bets (filterable)

### Other Endpoints
- `GET /api/drivers/` - List active drivers
- `GET /api/bet-types/` - List active bet types
- `GET /api/profiles/me/` - Current user profile
- `GET /api/standings/` - Competition standings

## Management Commands

### Seed Database
```bash
python manage.py seed_data [--clear]
```
Populates the database with sample F1 data for testing.

### Load Race Results
```bash
python manage.py load_results --races 3
```
Loads sample race results for demonstration and testing purposes.

### Score Race
```bash
python manage.py score_race 1
```
Calculates points for all bets in a race and updates standings. Requires the race ID as an argument.

**Example workflow:**
1. Race finishes
2. Admin enters results in Django admin (or uses `load_results` command)
3. Run `python manage.py score_race 1` (where 1 is the race ID)
4. Standings automatically update

📚 **For detailed instructions, see the [Admin Tutorial](ADMIN_TUTORIAL.md)**

## Scoring System

The default scoring system awards:
- **10 points** - Exact position match (e.g., predicted P1, driver finished P1)
- **5 points** - Correct driver in top 10 (e.g., predicted P3, driver finished P7)
- **0 points** - Driver not in top 10 or incorrect prediction

Administrators can customize point values per competition.

## Deployment

### Azure App Service

1. **Create Azure Web App**
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name f1-betting-pool \
  --runtime "PYTHON:3.11"
```

2. **Configure environment variables**
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name f1-betting-pool \
  --settings \
    SECRET_KEY="your-secret-key" \
    DEBUG="False" \
    ALLOWED_HOSTS="your-domain.azurewebsites.net"
```

3. **Deploy**
```bash
az webapp up \
  --resource-group myResourceGroup \
  --name f1-betting-pool \
  --sku B1
```

### Production Checklist

**IMPORTANT:** Never use development settings (`DEBUG=True`) in production!

- [ ] Set `DEBUG=False` in production environment variables (this automatically enables all security features)
- [ ] Use strong `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Configure proper `ALLOWED_HOSTS` with your production domain
- [ ] Set up PostgreSQL or Azure SQL (migrate from SQLite)
- [ ] Configure email backend for MFA (Gmail SMTP, SendGrid, etc.)
- [ ] Set up social auth credentials (Google, GitHub)
- [ ] Verify HTTPS/SSL is working (automatically enforced when `DEBUG=False`)
- [ ] Set up automated backups
- [ ] Configure logging and monitoring
- [ ] Test that HTTP redirects to HTTPS
- [ ] Verify secure cookies are working

See the [Development vs Production Mode](#development-vs-production-mode) section for details on security settings.

## Design System

### Color Palette
- **Primary Red**: #DC0000 (Racing theme)
- **Secondary Blue**: #00D9FF (Electric, energetic)
- **Accent Gold**: #FFD700 (1st place)
- **Accent Silver**: #C0C0C0 (2nd place)
- **Accent Bronze**: #CD7F32 (3rd place)
- **Dark Backgrounds**: #0A0A0A to #4A4A4A
- **Status Colors**: Success, Warning, Error, Info

### Typography
- **Primary Font**: Inter (body text)
- **Display Font**: Rajdhani (headings, racing aesthetic)

### Components
Reusable components are defined in `/static/css/design-system.css`:
- Buttons (Primary, Secondary, Outline, Ghost)
- Cards (Standard, Racing-themed)
- Badges (Position, Status)
- Forms (Inputs, Selects, Textareas)
- Tables (Leaderboards, results)
- Modals
- Loading states

## Future Enhancements

- [ ] Additional bet types (Podium, Winner, Pole Position, Fastest Lap)
- [ ] Live race updates via WebSockets
- [ ] Email notifications for race results and standings
- [ ] Mobile app (React Native)
- [ ] Private/public competitions
- [ ] Betting history analytics and statistics
- [ ] Social features (comments, chat)
- [ ] Multi-sport support (MotoGP, NASCAR, etc.)
- [ ] Betting marketplace/trading
- [ ] Achievement badges and rewards

## Development

### Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests with pytest (recommended):
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=betting --cov-report=html
```

📚 **For detailed testing information, see [TESTING.md](TESTING.md)**

### Continuous Integration

The project uses GitHub Actions for automated testing:
- ✅ Test suite on Python 3.11 & 3.12
- ✅ Code quality checks (flake8, black, isort)
- ✅ Security scanning (safety, bandit)
- ✅ Integration tests
- ✅ Performance tests
- ✅ Code coverage reports

### Code Quality

Format code:
```bash
black .
```

Lint code:
```bash
flake8 .
```

Sort imports:
```bash
isort .
```

Run all quality checks:
```bash
flake8 . && black --check . && isort --check-only .
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Development Dependencies

Install all development and testing dependencies:
```bash
pip install -r requirements-dev.txt
```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear
```

### Database issues
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py seed_data
```

### Authentication issues
Clear browser cookies and cache, then try logging in again.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

### Workflow Jobs
- **Test Suite** - Runs unit and integration tests on Python 3.11, 3.12, and 3.14
- **Code Quality** - Linting with flake8, formatting with black, import sorting with isort
- **Security Scan** - Vulnerability scanning with safety and bandit
- **Build Check** - Validates deployment readiness and static file collection
- **Integration Tests** - End-to-end workflow testing with seed data and race scoring
- **Performance Tests** - Database query performance analysis

### Status Badges
The badges at the top of this README show:
- **CI/CD Pipeline** - Overall workflow status (click to view details)
- **Code Coverage** - Test coverage percentage from Codecov
- **Python Versions** - Supported Python versions (3.11, 3.12, 3.14)
- **Django Version** - Current Django framework version
- **License** - Project license (MIT)
- **F1 Racing** - Theme indicator

All tests must pass before merging to main branch.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- F1 data provided by OpenF1 API
- Inspired by the excitement of Formula 1 racing
- Built for racing enthusiasts who love to compete

---

Built with ❤️ for F1 fans. Let the racing begin! 🏁
