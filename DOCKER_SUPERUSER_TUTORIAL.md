# Creating a Django Superuser in Docker

This tutorial shows you how to create a Django superuser account for your F1 Betting Pool application running in Docker.

## Prerequisites

- Docker containers must be running (check with `docker-compose ps`)
- Both `f1betting-web` and `f1betting-db` containers should show as "healthy"

## Step 1: Verify Containers Are Running

First, make sure your Docker containers are up and running.

**For Windows PowerShell:**
```powershell
docker-compose --env-file .env ps
```

**For Git Bash / WSL / Linux / macOS:**
```bash
set -a && source .env && set +a && docker-compose ps
```

You should see both containers with STATUS showing "Up" and "healthy":
```
NAME            STATUS
f1betting-db    Up X seconds (healthy)
f1betting-web   Up X seconds (healthy)
```

**Note:** If containers aren't running, start them with:
- **Windows PowerShell:** `docker-compose --env-file .env up -d`
- **Git Bash / Linux / macOS:** `set -a && source .env && set +a && docker-compose up -d`

## Step 2: Access the Container Shell

Open an interactive bash shell inside the web container:

```bash
docker exec -it f1betting-web bash
```

You should see a prompt like this:
```
appuser@<container-id>:/app$
```

## Step 3: Run the Superuser Creation Command

Inside the container, run Django's createsuperuser command:

```bash
python manage.py createsuperuser
```

## Step 4: Fill in the Superuser Details

The command will prompt you for the following information:

### Username
```
Username: admin
```
(Or choose any username you prefer)

### Email Address
```
Email address: admin@example.com
```
(Use a valid email address if you plan to use email features)

### Password
```
Password: ********
Password (again): ********
```

**Password Requirements:**
- Cannot be too similar to your username or email
- Must contain at least 8 characters
- Cannot be entirely numeric
- Cannot be a commonly used password

**Example:**
- Good password: `MySecurePass123!`
- Bad password: `admin123` (too simple)

## Step 5: Confirm Success

If successful, you'll see:
```
Superuser created successfully.
```

## Step 6: Exit the Container

Type `exit` to leave the container shell:
```bash
exit
```

## Step 7: Test Your Superuser Account

1. Open your browser and navigate to: http://localhost:8000/admin
2. Log in with the username and password you just created
3. You should see the Django admin interface

## Troubleshooting

### Container is restarting
If you get an error like "Container is restarting", wait a few seconds and try again:
```bash
docker-compose logs web
```

Check the logs for any errors and wait until the container is stable.

### Command not found
If `python` command is not found, try:
```bash
python3 manage.py createsuperuser
```

### Password validation errors
If your password is rejected, try a stronger password with:
- Mix of uppercase and lowercase letters
- Numbers
- Special characters (!@#$%^&*)
- At least 8 characters long

## Alternative: Non-Interactive Method

If the interactive method doesn't work, you can create a superuser programmatically:

```bash
docker exec -it f1betting-web bash
```

Then inside the container:

```bash
python manage.py shell
```

In the Python shell:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='YourSecurePassword123!'
)
print(f"Superuser {user.username} created successfully!")
exit()
```

Then exit the container:
```bash
exit
```

## Next Steps

After creating your superuser:

1. Log in to the admin panel: http://localhost:8000/admin
2. Create your F1 betting competitions
3. Add drivers, teams, and races
4. Invite users to join your betting pool

## Security Tips

- **Never** use simple passwords like "admin123" in production
- Change the default superuser password after first login
- Use a unique email address for the admin account
- Consider enabling two-factor authentication if available
