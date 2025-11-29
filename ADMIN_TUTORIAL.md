# F1 Betting Pool - Admin Tutorial

Welcome to the F1 Betting Pool Admin Tutorial! This step-by-step guide will walk you through all the administrative tasks needed to run your F1 betting pool successfully.

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Understanding the Statistics Dashboard](#2-understanding-the-statistics-dashboard)
3. [Setting Up a New Season](#3-setting-up-a-new-season)
4. [Managing Drivers](#4-managing-drivers)
5. [Creating a Competition](#5-creating-a-competition)
6. [Setting Up Races](#6-setting-up-races)
7. [Managing Bet Types](#7-managing-bet-types)
8. [Managing Users](#8-managing-users)
9. [Loading Race Results](#9-loading-race-results)
10. [Scoring Races](#10-scoring-races)
11. [Viewing Standings](#11-viewing-standings)
12. [Troubleshooting](#12-troubleshooting)
13. [Best Practices](#13-best-practices)

---

## 1. Getting Started

### Step 1: Access the Admin Panel

1. Navigate to your site's admin URL: `http://your-domain.com/admin/`
2. Log in with your admin credentials:
   - **Email:** `admin@f1betting.com`
   - **Password:** `admin123` (change this immediately in production!)

### Step 2: Change Your Admin Password (Important!)

1. Click on **"Users"** in the admin menu
2. Find and click on your admin user account
3. Scroll down to the password section
4. Click **"this form"** next to "Raw passwords are not stored"
5. Enter your new password twice
6. Click **"Save"**

### Step 3: Familiarize Yourself with the Admin Interface

The admin panel has several sections:
- **Authentication and Authorization:** Manage users and groups
- **Betting:** All F1 betting pool models (Competitions, Races, Drivers, Bets, etc.)

---

## 2. Understanding the Statistics Dashboard

When you first log in, you'll see a comprehensive statistics dashboard at the top of the admin homepage.

### Dashboard Sections

#### Core Entities
- **Users:** Total users, active users, superusers, groups, and users with bets
- **Competitions:** Total and active competitions
- **Drivers:** Total, active, and inactive drivers

#### Racing Data
- **Races:** Total, completed, upcoming, and pending races
- **Race Results:** Total and verified results

#### Betting Activity
- **Bets:** Total, scored, and unscored bets
- **Bet Types:** Total and active bet types
- **Standings:** Total standing entries

**Tip:** The dashboard updates every time you load the admin homepage, giving you real-time insights!

---

## 3. Setting Up a New Season

### Option A: Use the Seed Data Command (Recommended for Testing)

If you're setting up the system for the first time or testing:

```bash
python manage.py seed_data
```

This automatically creates:
- 20 F1 drivers (2025 lineup)
- Default bet types
- A 2025 competition
- 24 races with the 2025 calendar
- 5 test users

### Option B: Manual Setup (For Production)

Follow steps 4-7 in order to manually set up your season.

---

## 4. Managing Drivers

### Adding a New Driver

1. Click **"Drivers"** in the admin menu
2. Click **"Add Driver"** in the top right
3. Fill in the required fields:
   - **Driver Number:** The driver's racing number (e.g., 44 for Hamilton)
   - **First Name:** Driver's first name
   - **Last Name:** Driver's last name
   - **Team:** Current team (e.g., Ferrari, Red Bull Racing, McLaren)
   - **Nationality:** Driver's nationality (e.g., British, Dutch, Spanish)
   - **Is Active:** Check this box for current drivers
4. Click **"Save"**

### Editing a Driver

1. Click **"Drivers"** in the admin menu
2. Find the driver you want to edit
3. Click on their name
4. Make your changes
5. Click **"Save"**

### Deactivating a Driver

When a driver leaves F1 or changes mid-season:
1. Edit the driver
2. Uncheck **"Is Active"**
3. Click **"Save"**

**Note:** Don't delete drivers who have existing bets or results!

### Bulk Import Drivers (Advanced)

For the current 2025 season, you can use the seed command:

```bash
python manage.py seed_data
```

This will add all 20 current F1 drivers.

---

## 5. Creating a Competition

A competition represents an entire F1 season.

### Step 1: Create the Competition

1. Click **"Competitions"** in the admin menu
2. Click **"Add Competition"** in the top right
3. Fill in the details:

#### Basic Information
- **Name:** e.g., "F1 2025 World Championship"
- **Description:** Brief description of the competition
- **Year:** 2025
- **Status:** Select "Active" to open it for users

#### Dates
- **Start Date:** First race date (e.g., March 16, 2025)
- **End Date:** Last race date (e.g., December 7, 2025)

#### Points Configuration
- **Points for Exact Position:** Points awarded for predicting the exact finishing position (default: 10)
- **Points for Correct Driver:** Points for predicting a driver in the top 10 but wrong position (default: 5)

#### Management
- **Created By:** Select yourself as the admin
- **Participants:** Leave empty for now (users join themselves)

4. Click **"Save"**

### Step 2: Publish the Competition

Users can only see competitions with status "Active". Make sure to set the status to "Active" after creating all the races.

---

## 6. Setting Up Races

### Adding a Single Race

1. Click **"Races"** in the admin menu
2. Click **"Add Race"** in the top right
3. Fill in the race information:

#### Race Information
- **Competition:** Select your 2025 competition
- **Name:** e.g., "Bahrain Grand Prix"
- **Location:** e.g., "Sakhir"
- **Country:** e.g., "Bahrain"
- **Round Number:** The race number in the season (1-24)

#### Schedule
- **Race Datetime:** Date and time of the race start (use your timezone)
- **Betting Deadline:** When betting closes (typically race start time)

#### Status
- **Status:**
  - "Scheduled" - Race hasn't happened yet
  - "Completed" - Race is finished and results are in
  - "Cancelled" - Race was cancelled

4. Click **"Save"**

### Bulk Adding Races

The quickest way to set up all races for a season:

```bash
python manage.py seed_data
```

This creates all 24 races of the 2025 F1 calendar with correct dates.

### Important Deadline Notes

- Set betting deadlines carefully! Users cannot place bets after the deadline.
- The system automatically checks if betting is still open using the `is_betting_open()` method
- You can close betting early by setting status to "Completed"

---

## 7. Managing Bet Types

Bet types define what users can bet on. The system comes with several pre-configured types.

### Default Bet Types

The following bet types are created automatically by `seed_data`:

1. **Top 10 Finish** (code: `top10`)
   - Users predict all 10 drivers finishing in the top 10
   - Requires positions: Yes
   - Max selections: 10

2. **Podium** (code: `podium`)
   - Users predict the top 3 finishers
   - Requires positions: Yes
   - Max selections: 3

3. **Race Winner** (code: `winner`)
   - Users predict the race winner
   - Requires positions: No
   - Max selections: 1

4. **Pole Position** (code: `pole`)
   - Users predict who gets pole position in qualifying
   - Requires positions: No
   - Max selections: 1

5. **Fastest Lap** (code: `fastest_lap`)
   - Users predict who sets the fastest lap
   - Requires positions: No
   - Max selections: 1

6. **DNF Prediction** (code: `dnf`)
   - Users predict drivers who won't finish
   - Requires positions: No
   - Max selections: Up to driver's choice

### Adding a Custom Bet Type

1. Click **"Bet Types"** in the admin menu
2. Click **"Add Bet Type"** in the top right
3. Fill in the details:
   - **Name:** Display name (e.g., "Fastest Pit Stop")
   - **Code:** Unique identifier (e.g., "fastest_pit")
   - **Description:** Explain the bet type
   - **Requires Positions:** Check if users need to specify finishing positions
   - **Max Selections:** Maximum number of selections allowed
   - **Is Active:** Check to enable this bet type
4. Click **"Save"**

### Deactivating a Bet Type

1. Find the bet type in the list
2. Click on it
3. Uncheck **"Is Active"**
4. Click **"Save"**

**Note:** Users won't be able to place new bets of this type, but existing bets remain.

---

## 8. Managing Users

### Viewing Users

1. Click **"Users"** in the admin menu
2. You'll see a list of all registered users

### User Information Includes:
- **Email address** (used for login)
- **Display name** (from UserProfile)
- **Active status**
- **Staff status** (can access admin)
- **Superuser status** (full admin rights)

### Making a User an Admin

1. Click **"Users"** in the admin menu
2. Click on the user you want to promote
3. Scroll to the **"Permissions"** section
4. Check **"Staff status"** (allows admin access)
5. Optionally check **"Superuser status"** (full permissions)
6. Click **"Save"**

### Managing User Profiles

Each user has a profile with additional information:

1. Click **"Users"** in the admin menu
2. Click on a user
3. Scroll down to the **"Profile"** section (inline form)
4. You can edit:
   - **Display Name:** Their public name
   - **Avatar:** Profile picture (upload)
   - **Total Points:** Read-only, calculated from standings

### Deactivating a User

1. Edit the user
2. Uncheck **"Active"** in the permissions section
3. Click **"Save"**

The user won't be able to log in, but their bets and data remain.

### Viewing User's Bets

1. Click **"Bets"** in the admin menu
2. Use the filter on the right to filter by user email
3. You'll see all their bets across all races

---

## 9. Loading Race Results

After a race finishes, you need to load the results into the system.

### Option A: Use the Load Results Command (Recommended)

For testing or loading sample data:

```bash
# Load results for the first 3 races
python manage.py load_results --races 3

# Load results for the first 5 races
python manage.py load_results --races 5
```

This command:
- Loads realistic sample results based on driver/team performance
- Automatically marks races as "Completed"
- Creates all top 10 results for each race
- Marks results as "Verified"

### Option B: Manual Entry (For Actual Races)

#### Step 1: Add Race Results

1. Click **"Race Results"** in the admin menu
2. Click **"Add Race Result"** in the top right
3. Fill in the details:

##### Result Information
- **Race:** Select the race
- **Driver:** Select the driver
- **Position:** Finishing position (1-20)

##### Additional Data
- **Grid Position:** Starting position in the race
- **Fastest Lap:** Check if they set the fastest lap
- **Did Not Finish:** Check if they DNF'd
- **DNF Reason:** If DNF, explain why (e.g., "Engine failure")

##### Verification
- **Verified:** Check this box once you've confirmed the result is accurate

4. Click **"Save and add another"** to add the next result
5. Repeat for all top 10 finishers (or all finishers if desired)

#### Step 2: Mark the Race as Completed

1. Click **"Races"** in the admin menu
2. Find and click on the race
3. Change **Status** to "Completed"
4. Click **"Save"**

### Important Notes

- Always enter at least the top 10 finishers for proper scoring
- Make sure to mark results as "Verified" when confirmed
- Don't delete or modify results after scoring (scores won't recalculate automatically)

---

## 10. Scoring Races

After loading race results, you need to score all the bets to calculate points.

### Using the Score Race Command

```bash
# Score a specific race by its database ID
python manage.py score_race 1
```

The command will:
1. Find all unscored bets for that race
2. Compare each bet against the actual results
3. Award points:
   - **10 points:** Driver predicted in exact position
   - **5 points:** Driver predicted in top 10 but different position
   - **0 points:** Driver not in top 10 or wrong
4. Update competition standings with total points and ranks
5. Display the updated leaderboard

### Manual Scoring (Not Recommended)

You can manually update bet points through the admin interface, but this is error-prone:

1. Click **"Bets"** in the admin menu
2. Filter by the race
3. Click on each bet
4. Manually enter **"Points Earned"**
5. Check **"Is Scored"**
6. Click **"Save"**

**Warning:** Manual scoring doesn't update competition standings automatically!

### Verifying Scoring

After scoring, check:

1. **Bets:** Filter by race and verify "Is Scored" is checked
2. **Competition Standings:** Check that ranks and points look correct
3. **Statistics Dashboard:** Verify the scored/unscored bet counts

---

## 11. Viewing Standings

### Competition Standings in Admin

1. Click **"Competition Standings"** in the admin menu
2. Filter by competition using the filter on the right
3. You'll see:
   - **Rank:** Current position in the competition
   - **User:** The user's email
   - **Competition:** Which season
   - **Total Points:** Their cumulative points
   - **Races Predicted:** How many races they've bet on
   - **Exact Predictions:** Count of perfectly predicted positions

### Standings are Updated When:
- You run the `score_race` command
- The scoring system recalculates after a race is scored
- Rankings are ordered by total points (highest first)

### Leaderboard for Users

Users can view standings through the web interface:
1. Log in to the site (not admin)
2. Navigate to the "Leaderboard" section
3. They'll see their rank, points, and compare with other users

---

## 12. Troubleshooting

### Issue: Users Can't See the Competition

**Solution:**
1. Go to **Competitions**
2. Edit your competition
3. Make sure **Status** is set to "Active"
4. Save

### Issue: Users Can't Place Bets

**Possible Causes:**

1. **Betting Deadline Passed:**
   - Check the race's **Betting Deadline** hasn't passed
   - Edit the race and extend the deadline if needed

2. **Race Status is Completed:**
   - Check **Status** in the race
   - Change to "Scheduled" if betting should still be open

3. **Bet Type is Inactive:**
   - Go to **Bet Types**
   - Make sure **Is Active** is checked

### Issue: Scoring Command Shows "No unscored bets found"

**Possible Causes:**

1. **No Users Placed Bets:**
   - Check **Bets** to confirm users have placed bets for that race

2. **Bets Already Scored:**
   - Filter bets by race and check "Is Scored" status
   - If already scored, the command won't re-score (by design)

3. **Race Results Not Loaded:**
   - Go to **Race Results** and verify top 10 results exist for the race

### Issue: Statistics Dashboard Shows Wrong Numbers

**Solution:**
- Refresh the admin homepage (Ctrl+F5 or Cmd+Shift+R)
- Statistics are calculated on page load, not cached

### Issue: Login Page Shows Template Error

**Solution:**
- Check that django-allauth is properly installed
- Verify `{% load socialaccount %}` and `{% get_providers as socialaccount_providers %}` are at the top of the template
- Run `python manage.py migrate` to ensure all allauth tables exist

### Issue: Static Files (CSS) Not Loading

**Solution:**

1. **In Development:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Check Settings:**
   - Verify `DEBUG = True` for development
   - Check `ALLOWED_HOSTS` includes your domain

3. **Hard Refresh Browser:**
   - Windows/Linux: Ctrl+F5
   - Mac: Cmd+Shift+R

---

## 13. Best Practices

### Before the Season Starts

1. **Set Up All Infrastructure:**
   - Load all drivers for the current season
   - Create the competition
   - Set up all 24 races with correct dates and times
   - Verify all bet types are active

2. **Test the System:**
   - Create a test competition
   - Place test bets as a regular user
   - Load sample results
   - Score the test race
   - Verify standings update correctly

3. **Communicate with Users:**
   - Send them the site URL
   - Provide test credentials for practice
   - Explain the rules and points system
   - Set expectations for when betting closes

### During the Season

1. **Before Each Race:**
   - Verify the betting deadline is correct (check for timezone issues!)
   - Remind users to place their bets
   - Check that the race shows in the "Races" page

2. **After Each Race:**
   - Load results as soon as possible (users want to see their scores!)
   - Double-check results before marking as "Verified"
   - Run the scoring command
   - Verify the leaderboard updated correctly
   - Post a message/email to users about the results

3. **Weekly Maintenance:**
   - Check the statistics dashboard for anomalies
   - Review unscored bets (should be zero after scoring)
   - Verify upcoming race deadlines are correct
   - Backup your database

### Security Best Practices

1. **Change Default Passwords:**
   - Change admin password immediately
   - Change all test user passwords or delete them in production

2. **Use Strong Passwords:**
   - Minimum 12 characters
   - Mix of letters, numbers, symbols
   - Use a password manager

3. **Regular Backups:**
   ```bash
   # Backup the database
   python manage.py dumpdata > backup_$(date +%Y%m%d).json

   # Or backup SQLite file directly
   cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
   ```

4. **Update Settings for Production:**
   - Set `DEBUG = False`
   - Use environment variables for secrets
   - Set proper `ALLOWED_HOSTS`
   - Use HTTPS in production

### Points System Tips

The default points are:
- **10 points:** Exact position match
- **5 points:** Correct driver, wrong position

You can adjust these in the Competition settings. Consider:
- Higher points for exact matches encourages precision
- Lower partial points makes competition closer
- Very high partial points can lead to predictable winners

Test different configurations with sample data before the season!

### Managing Disputes

If users dispute scores:

1. **Verify Race Results:**
   - Check official F1 results
   - Confirm your **Race Results** entries are accurate

2. **Check Their Bet:**
   - Go to **Bets**
   - Filter by user and race
   - Verify their predictions

3. **Manually Adjust if Needed:**
   - Edit the bet
   - Adjust **Points Earned**
   - Add a note in the admin log
   - Re-run scoring for the race if needed

4. **Communicate:**
   - Explain the scoring logic
   - Show them the results vs their bet
   - Be transparent about any adjustments

---

## Quick Reference Commands

```bash
# Set up initial data (drivers, races, bet types, test users)
python manage.py seed_data

# Load sample race results (for first N races)
python manage.py load_results --races 3

# Score a specific race (by race ID)
python manage.py score_race 1

# Backup database
python manage.py dumpdata > backup.json

# Collect static files
python manage.py collectstatic --noinput

# Create a new admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Getting Help

### Documentation
- **README.md:** General project information and setup
- **QUICKSTART.md:** Quick setup guide
- **ADMIN_TUTORIAL.md:** This file!

### Common Resources
- **Django Admin Documentation:** https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
- **Django AllAuth Documentation:** https://django-allauth.readthedocs.io/

### Need More Help?

Contact the development team or check the project repository for updates and support.

---

**Good luck running your F1 Betting Pool! 🏎️🏁**
