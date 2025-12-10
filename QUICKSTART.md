# Quick Start Guide - F1 Betting Pool

## Get Started in 5 Minutes!

> **💡 Running on Your Laptop?** This application is pre-configured for local development without HTTPS! Just run `python manage.py run dev` - no SSL certificates or HTTPS setup required. The system automatically runs on `http://localhost:8000` in development mode.

### Step 1: Install Dependencies
```bash
# Activate virtual environment (already created)
source venv/bin/activate

# Dependencies are already installed, but if you need to reinstall:
# pip install -r requirements.txt
```

### Step 2: Start the Development Server

**Method 1: Using the `run` command (Recommended)**
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

**Method 2: Using environment files (Traditional)**
```bash
# Copy the development environment configuration
cp .env.development .env

# Then start the server
python manage.py runserver
```

**No additional configuration needed!** The `run dev` command handles everything automatically.

### Step 3: Access the Application
Open your browser and visit:
- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

**Pre-loaded Test Data:**
- Admin user: `admin@f1betting.com` / `admin123`
- Test users: `user1@test.com` to `user5@test.com` / `test123`
- 20 F1 drivers (2024 grid)
- 2025 F1 Championship with 24 races

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
