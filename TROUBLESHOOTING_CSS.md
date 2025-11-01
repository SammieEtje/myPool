# Fixing CSS/Static Files Issues

## Quick Fix for Missing CSS

If you see pages without styling (especially `/accounts/logout/`), follow these steps:

### Step 1: Collect Static Files
```bash
source venv/bin/activate
python manage.py collectstatic --noinput --clear
```

### Step 2: Clear Browser Cache
**Chrome/Edge:**
- Press `Ctrl + Shift + Delete` (Windows/Linux) or `Cmd + Shift + Delete` (Mac)
- Select "Cached images and files"
- Click "Clear data"

**Or use Hard Refresh:**
- `Ctrl + F5` (Windows/Linux)
- `Cmd + Shift + R` (Mac)

### Step 3: Restart Server
```bash
# Stop the server (Ctrl+C)
python manage.py runserver
```

### Step 4: Test in Incognito/Private Mode
- Chrome: `Ctrl + Shift + N`
- Firefox: `Ctrl + Shift + P`
- Safari: `Cmd + Shift + N`

This bypasses all cache and ensures you see the latest version.

## Verification Test

Run this test to verify templates are working:

```bash
python << 'EOF'
import os, sys, django
sys.path.insert(0, '/home/user/myPool')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'f1betting.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.filter(email='user1@test.com').first()
if user:
    client.force_login(user)
    response = client.get('/accounts/logout/')

    checks = {
        'Page loads': response.status_code == 200,
        'Custom template used': b'Are you sure you want to sign out?' in response.content,
        'CSS linked': b'design-system.css' in response.content,
        'Racing theme': b'auth-container' in response.content,
    }

    print("\nLogout Page Tests:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")

    if all(checks.values()):
        print("\n🎉 All tests passed! The logout page is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
else:
    print("❌ No test user found. Run: python manage.py seed_data")
EOF
```

## Common Issues & Solutions

### Issue 1: "Page loads but no styling"
**Symptoms:** White background, plain text, no colors
**Solution:**
```bash
# Clear static files and re-collect
rm -rf staticfiles/
python manage.py collectstatic --noinput
python manage.py runserver
```
Then hard refresh your browser (`Ctrl+F5`)

### Issue 2: "404 on CSS files"
**Symptoms:** Browser console shows 404 errors for .css files
**Check:**
```bash
ls -la static/css/
# Should show: design-system.css and main.css
```

**Fix:**
```bash
# Make sure static files exist and have correct permissions
chmod -R 755 static/
python manage.py collectstatic --noinput
```

### Issue 3: "Logout redirects immediately"
**Symptoms:** Can't see logout confirmation page
**Solution:** This is now fixed with `ACCOUNT_LOGOUT_ON_GET = False`

The logout page will show confirmation before logging out.

### Issue 4: "CSS works on login but not logout"
**Symptoms:** Login page styled, logout page not styled
**Solution:**
```bash
# Verify template exists
ls templates/account/logout.html

# Check it extends base.html
head -1 templates/account/logout.html
# Should show: {% extends "account/base.html" %}
```

## Development Mode Static Files

Django serves static files automatically in development when `DEBUG=True`.

Verify settings:
```bash
python manage.py shell << 'EOF'
from django.conf import settings
print("DEBUG:", settings.DEBUG)
print("STATIC_URL:", settings.STATIC_URL)
print("STATICFILES_DIRS:", settings.STATICFILES_DIRS)
EOF
```

Should output:
```
DEBUG: True
STATIC_URL: /static/
STATICFILES_DIRS: [PosixPath('/home/user/myPool/static')]
```

## Production Checklist

For production deployment:

1. ✅ Run `collectstatic`:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. ✅ Configure web server to serve `/static/` and `/media/`

3. ✅ Set `DEBUG = False` in production

4. ✅ Use proper `ALLOWED_HOSTS`

5. ✅ Consider using CDN for static files

## Still Having Issues?

If CSS still doesn't load:

1. **Check browser console** (F12) for errors
2. **Verify file paths:**
   ```bash
   find static -name "*.css"
   find staticfiles -name "*.css"
   ```
3. **Test static file serving:**
   - Start server
   - Visit: http://localhost:8000/static/css/design-system.css
   - Should download or display the CSS file

4. **Check Django settings:**
   ```python
   # In settings.py, verify:
   STATIC_URL = "/static/"
   STATICFILES_DIRS = [BASE_DIR / "static"]
   ```

## Final Test

Visit these URLs and verify styling:
- ✅ http://localhost:8000/ (Main app)
- ✅ http://localhost:8000/accounts/login/ (Login)
- ✅ http://localhost:8000/accounts/signup/ (Signup)
- ✅ http://localhost:8000/accounts/logout/ (Logout - AFTER logging in)
- ✅ http://localhost:8000/admin (Admin)

All should have the racing-themed design with dark background, red/blue colors.

---

**If all else fails:** Delete `db.sqlite3`, run `python manage.py migrate && python manage.py seed_data`, and start fresh!
