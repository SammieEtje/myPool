# Authentication Guide - F1 Betting Pool

## Login Credentials

### Admin Account
- **URL**: http://localhost:8000/admin
- **Email**: `admin@f1betting.com`
- **Password**: `admin123`
- **Access**: Full admin panel access

### Test User Accounts
- **URL**: http://localhost:8000/accounts/login/
- **Credentials**:
  - `user1@test.com` / `test123`
  - `user2@test.com` / `test123`
  - `user3@test.com` / `test123`
  - `user4@test.com` / `test123`
  - `user5@test.com` / `test123`

## Authentication Pages

All authentication pages now have a beautiful racing-themed design that matches the main application:

### Available Pages

1. **Login** - `/accounts/login/`
   - Email-based authentication
   - Remember me option
   - Password reset link
   - Test credentials displayed on page

2. **Sign Up** - `/accounts/signup/`
   - Create new account
   - Email and password validation
   - Automatic redirect after signup

3. **Logout** - `/accounts/logout/`
   - Confirmation page
   - Clean logout process

4. **Password Reset** - `/accounts/password/reset/`
   - Email-based password recovery
   - (Note: In development, emails are printed to console)

## Design Features

### Racing Theme
- 🏎️ F1 logo and branding
- 🔴 Racing red primary color
- 💙 Electric blue secondary color
- ⚫ Dark theme background
- ✨ Smooth animations and transitions

### User Experience
- ✅ Clear error messages
- ✅ Validation feedback
- ✅ Test credentials visible on login page
- ✅ Back to home link
- ✅ Mobile-responsive design
- ✅ High contrast for readability

## Social Login (Optional)

Social login is configured but requires API credentials:

### Google OAuth
1. Get credentials from https://console.cloud.google.com
2. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-secret
   ```
3. Add authorized redirect: `http://localhost:8000/accounts/google/login/callback/`

### GitHub OAuth
1. Get credentials from https://github.com/settings/developers
2. Add to `.env`:
   ```
   GITHUB_CLIENT_ID=your-client-id
   GITHUB_CLIENT_SECRET=your-secret
   ```
3. Add callback URL: `http://localhost:8000/accounts/github/login/callback/`

## Multi-Factor Authentication (MFA)

MFA is enabled and can be configured per user:

1. Login to your account
2. Go to Account Settings (when implemented)
3. Enable Two-Factor Authentication
4. Scan QR code with authenticator app (Google Authenticator, Authy, etc.)

## Development Notes

### Email Backend
In development, emails are printed to console instead of being sent:
```bash
# Check console output for password reset emails
python manage.py runserver
```

For production, configure SMTP settings in `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Quick Test Workflow

1. **Start Server**
   ```bash
   python manage.py runserver
   ```

2. **Test Login**
   - Visit http://localhost:8000/accounts/login/
   - Use: `user1@test.com` / `test123`
   - Should redirect to home page

3. **Test Signup**
   - Visit http://localhost:8000/accounts/signup/
   - Create new account with your email
   - Verify account creation

4. **Test Admin**
   - Visit http://localhost:8000/admin
   - Login: `admin@f1betting.com` / `admin123`
   - Access full admin panel

## Troubleshooting

### Issue: "Email address is not verified"
**Solution**: In development, email verification is optional. You can login immediately after signup.

### Issue: "Invalid login credentials"
**Solution**: Make sure you're using the EMAIL address, not username:
- ❌ Wrong: `testuser1`
- ✅ Correct: `user1@test.com`

### Issue: "Authentication pages have no styling"
**Solution**: Make sure static files are loaded:
```bash
python manage.py collectstatic --clear
# Then restart server
python manage.py runserver
```

### Issue: "Password reset email not received"
**Solution**: In development, check the console output where you ran `runserver`. The email will be printed there.

## Security Notes

### For Development
- Test passwords are simple (`test123`) - **DO NOT use in production**
- Admin password is default - **CHANGE in production**
- Debug mode is enabled - **DISABLE in production**

### For Production
- Use strong passwords (minimum 12 characters)
- Enable MFA for admin accounts
- Configure real email backend
- Set up HTTPS/SSL
- Use secure SECRET_KEY
- Set DEBUG=False
- Configure ALLOWED_HOSTS

## Template Customization

All authentication templates are in `/templates/account/`:
- `base.html` - Base template with styling
- `login.html` - Login form
- `signup.html` - Registration form
- `logout.html` - Logout confirmation
- `password_reset.html` - Password reset form

Customize colors and text by editing these templates!

---

**You're all set!** The authentication system is fully styled and ready to use. 🏁
