# Quick Start Guide - F1 Betting Pool

## Get Started in 5 Minutes!

Choose your preferred method: **Docker** (fastest, recommended) or **Local Development** (traditional).

---

## Method 1: Docker (Recommended - Fastest!)

**No Python setup required!** Docker handles everything for you.

### Prerequisites
- Docker and Docker Compose installed
- That's it!

### Step 1: Start with Docker Compose
```bash
# 1. Copy environment template
cp .env.production.template .env.production

# 2. Edit .env.production (set SECRET_KEY and POSTGRES_PASSWORD at minimum)
nano .env.production  # or use your preferred editor

# 3. Start everything with one command
docker-compose --env-file .env.production up -d

# 4. Create admin user
docker-compose exec web python manage.py createsuperuser
```

### Step 2: Access the Application
- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

**That's it!** Your F1 Betting Pool is running with PostgreSQL, all dependencies installed automatically.

### Useful Docker Commands
```bash
# View logs
docker-compose logs -f web

# Stop the application
docker-compose down

# Restart services
docker-compose restart

# Seed database with test data
docker-compose exec web python manage.py seed_data

# Score a race
docker-compose exec web python manage.py score_race 1

# Access Django shell
docker-compose exec web python manage.py shell
```

📚 **For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)**

---

## Method 2: Local Development (Traditional)

> **💡 Running on Your Laptop?** This application is pre-configured for local development without HTTPS! Just run `python manage.py run dev` - no SSL certificates or HTTPS setup required.

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Step 1: Install Dependencies
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Database
```bash
# Run migrations
python manage.py migrate

# Seed with test data (optional but recommended)
python manage.py seed_data
```

### Step 3: Start the Development Server

**Option A: Using the `run` command (Easiest)**
```bash
# Start the server in development mode
python manage.py run dev

# This automatically:
# ✅ Disables HTTPS/SSL requirements
# ✅ Runs on http://localhost:8000
# ✅ Uses SQLite (no database server needed)
# ✅ Prints emails to console (no SMTP setup needed)
# ✅ Shows a helpful configuration banner
```

**Option B: Using environment files (Traditional)**
```bash
# Copy the development environment configuration
cp .env.development .env

# Then start the server
python manage.py runserver
```

**No additional configuration needed!** The `run dev` command handles everything automatically.

### Step 4: Access the Application
Open your browser and visit:
- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

**Pre-loaded Test Data (if you ran seed_data):**
- Admin user: `admin@f1betting.com` / `admin123`
- Test users: `user1@test.com` to `user5@test.com` / `test123`
- 20 F1 drivers (2025 grid)
- 2025 F1 Championship with 24 races

---

## What You Can Do Now

### As a User (Frontend):
1. **Sign Up/Login** - Create an account or login with test credentials
2. **Browse Competitions** - View available F1 championships
3. **Join Competition** - Click "Join Competition" to participate
4. **Place Bets** - Go to "Races" and click "Place Bet" on upcoming races
5. **View Leaderboard** - Check your ranking against other users
6. **Track Your Bets** - See all your predictions in "My Bets"

### As an Admin (Admin Panel):
1. Login at http://localhost:8000/admin with `admin` / `admin123`
2. **Manage Competitions** - Create new seasons, edit existing ones
3. **Add Races** - Set race dates and betting deadlines
4. **Manage Drivers** - Add/edit driver information
5. **Enter Results** - After a race, add the actual finishing positions
6. **Score Race** - Run command to calculate points

## Typical Workflow

### For Administrators:

1. **Create a Competition**
   - Go to Admin → Competitions → Add Competition
   - Set year, name, dates, and points configuration
   - Publish it

2. **Add Races**
   - Go to Admin → Races → Add Race
   - Link to competition
   - Set race date and betting deadline
   - Status: "betting_open"

3. **After Race Finishes**
   - Go to Admin → Race Results
   - Add top 10 finishers with positions
   - Mark as "verified"

4. **Score the Race**
   ```bash
   python manage.py score_race <race_id>
   ```
   This automatically:
   - Calculates points for all bets
   - Updates user standings
   - Updates leaderboard

### For Users:

1. **Join a Competition**
   - Browse competitions on homepage
   - Click "Join Competition"

2. **Place Bets Before Deadline**
   - Go to "Races" page
   - Find upcoming race with "Betting Open" status
   - Click "Place Bet"
   - Select your Top 10 finishing order
   - Submit

3. **Check Results**
   - After race is scored, view your points in "My Bets"
   - Check your ranking in "Leaderboard"

## Test Data Available

### Users
- **admin@f1betting.com** / admin123 (superuser)
- user1@test.com / test123
- user2@test.com / test123
- user3@test.com / test123
- user4@test.com / test123
- user5@test.com / test123

### Competition
- F1 2025 World Championship (24 races)
- All races set to "betting_open" status
- Races start March 1, 2025

### Drivers
20 current F1 drivers ready for betting

## Need to Reset?

```bash
# Clear and reseed database
python manage.py seed_data --clear

# Or completely reset
rm db.sqlite3
python manage.py migrate
python manage.py seed_data
```

## Next Steps

1. **Customize Colors**: Edit `/static/css/design-system.css`
2. **Add Your Branding**: Update logo and title in `/templates/index.html`
3. **Configure Social Auth**: Set up Google/GitHub OAuth in settings
4. **Set Up Email**: Configure email backend for MFA and notifications
5. **Deploy to Azure**: Follow instructions in README.md

## Common Commands

### For Docker Users
```bash
# View logs
docker-compose logs -f web

# Run management commands
docker-compose exec web python manage.py <command>

# Examples:
docker-compose exec web python manage.py seed_data
docker-compose exec web python manage.py score_race 1
docker-compose exec web python manage.py createsuperuser

# Stop/Start
docker-compose down
docker-compose up -d
```

### For Local Development Users
```bash
# Run development server (no HTTPS)
python manage.py run dev

# Run production server (HTTPS required)
python manage.py run prod

# Traditional runserver (uses .env settings)
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Seed database
python manage.py seed_data

# Score a race (after entering results)
python manage.py score_race 1

# Collect static files (for deployment)
python manage.py collectstatic
```

## Troubleshooting

**Getting "accessing the development server over HTTPS" errors?**
Your browser is trying to use HTTPS, but the dev server only supports HTTP.
```bash
# 1. Make sure you're using http:// (not https://)
http://localhost:8000   ✅ Correct
https://localhost:8000  ❌ Wrong

# 2. Clear browser HSTS cache:
# Chrome/Edge: chrome://net-internals/#hsts → Delete "localhost"
# Firefox: Delete SiteSecurityServiceState.txt from profile
# Safari: Clear all browsing data

# 3. Or use incognito/private window
```

**Getting HTTPS/SSL errors?**
Use the development mode command:
```bash
# Simply run in dev mode (easiest)
python manage.py run dev

# Or check your .env file contains DEBUG=True:
cp .env.development .env
python manage.py runserver
```

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Static files not loading?**
```bash
python manage.py collectstatic --clear
```

**Need to clear browser cache?**
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Del
- Safari: Cmd+Option+E

**Want to deploy to production?**
See the **[README.md](README.md#development-vs-production-mode)** for production deployment instructions. Never use `DEBUG=True` in production!

## Getting Help

- Check README.md for full documentation
- Review code comments in models.py and views.py
- Explore the admin panel to understand data structure

---

**You're all set! Start the server and enjoy your F1 betting pool!** 🏎️🏁
