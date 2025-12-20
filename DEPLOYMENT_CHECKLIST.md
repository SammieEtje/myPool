# Deployment Checklist

Complete checklist for deploying the F1 Betting Pool application with the new Tailwind CSS design system.

## Pre-Deployment

### 1. Code Quality
- [x] All legacy CSS files removed
- [x] Templates updated to use Tailwind classes
- [x] Tailwind CSS builds successfully (`npm run build:css`)
- [ ] All Python tests passing (`pytest`)
- [ ] Code formatted with Black
- [ ] No linting errors with Flake8

### 2. Static Files
- [x] `static/css/input.css` contains all custom components
- [x] `tailwind.config.js` has correct color palette
- [x] Fonts loaded (Inter, Rajdhani)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] All images optimized

### 3. Environment Configuration
- [ ] `.env` file configured for production
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` set correctly
- [ ] `SECRET_KEY` is strong and unique
- [ ] Database credentials secured
- [ ] Email settings configured (if using)

### 4. Database
- [ ] All migrations created (`python manage.py makemigrations`)
- [ ] All migrations applied (`python manage.py migrate`)
- [ ] Database backup created
- [ ] Superuser created

## Docker Deployment

### 5. Docker Build
- [x] `Dockerfile` updated with multi-stage build
- [x] `.dockerignore` configured
- [ ] Docker image builds successfully
  ```bash
  docker build -t f1betting:latest .
  ```
- [ ] Image size is reasonable (< 500MB recommended)
- [ ] Container runs without errors
  ```bash
  docker run -p 8000:8000 --env-file .env f1betting:latest
  ```

### 6. Docker Compose
- [ ] `docker-compose.yml` configured
- [ ] Database service configured
- [ ] Environment variables set
- [ ] All services start successfully
  ```bash
  docker-compose up -d
  ```
- [ ] Health checks passing
  ```bash
  docker-compose ps
  ```

### 7. Tailwind in Docker
- [ ] CSS builds during Docker build
- [ ] `output.css` exists in container
  ```bash
  docker-compose exec web ls -la static/css/
  ```
- [ ] Static files collected correctly
  ```bash
  docker-compose exec web ls -la staticfiles/css/
  ```

## Application Testing

### 8. Functionality
- [ ] Homepage loads correctly
- [ ] Navigation works
- [ ] Login/signup pages styled correctly
- [ ] Forms submit properly
- [ ] All pages responsive (mobile, tablet, desktop)
- [ ] No console errors in browser

### 9. Design System
- [ ] Primary color (#F64740) displays correctly
- [ ] Secondary color (#477998) displays correctly
- [ ] Dark backgrounds (#291F1E) render properly
- [ ] All component classes work:
  - [ ] Buttons (btn-primary, btn-secondary, etc.)
  - [ ] Cards
  - [ ] Forms
  - [ ] Badges
  - [ ] Navigation
  - [ ] Modals

### 10. Performance
- [ ] Page load time < 3 seconds
- [ ] CSS file size reasonable (< 50KB recommended)
- [ ] No unused CSS (Tailwind purges correctly)
- [ ] Images load quickly
- [ ] No memory leaks

## Security

### 11. Django Security
- [ ] `SECURE_SSL_REDIRECT=True` (production)
- [ ] `SECURE_HSTS_SECONDS` set (production)
- [ ] `SESSION_COOKIE_SECURE=True` (production)
- [ ] `CSRF_COOKIE_SECURE=True` (production)
- [ ] CORS configured correctly
- [ ] SQL injection prevention tested
- [ ] XSS prevention tested

### 12. Docker Security
- [ ] Container runs as non-root user
- [ ] No secrets in Dockerfile
- [ ] Image scanned for vulnerabilities
- [ ] Only necessary ports exposed
- [ ] Health checks configured

## Monitoring

### 13. Logging
- [ ] Application logs configured
- [ ] Error logging works
- [ ] Access logs enabled
- [ ] Log rotation configured

### 14. Health Checks
- [ ] `/health/` endpoint works
- [ ] Database connectivity checked
- [ ] Static files serve correctly
- [ ] Docker health checks passing

## Production Deployment

### 15. Pre-Deploy
- [ ] All environment variables set
- [ ] Database backed up
- [ ] Deploy tag/version created
- [ ] Rollback plan ready

### 16. Deploy
- [ ] Docker image built with version tag
  ```bash
  docker build -t f1betting:1.0.0 .
  ```
- [ ] Image pushed to registry (if applicable)
- [ ] Database migrations run
  ```bash
  docker-compose exec web python manage.py migrate
  ```
- [ ] Static files collected
- [ ] Application started
  ```bash
  docker-compose up -d
  ```

### 17. Post-Deploy
- [ ] All services running
- [ ] Health checks passing
- [ ] No errors in logs
- [ ] Homepage accessible
- [ ] Login works
- [ ] Admin panel accessible
- [ ] Email notifications working (if configured)

## Verification

### 18. Smoke Tests
- [ ] Can view competitions
- [ ] Can view races
- [ ] Can place a bet
- [ ] Can view leaderboard
- [ ] Can login/logout
- [ ] Can signup new user
- [ ] Password reset works
- [ ] Admin panel accessible

### 19. Cross-Browser
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (if applicable)
- [ ] Mobile browsers

### 20. Responsive Design
- [ ] Mobile (< 768px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (> 1024px)
- [ ] Large screens (> 1920px)

## Documentation

### 21. Updated Docs
- [x] `TAILWIND.md` - Tailwind usage guide
- [x] `DOCKER.md` - Docker deployment guide
- [x] `DESIGN_MIGRATION.md` - Migration documentation
- [x] `CLAUDE.md` - Development guidelines
- [x] `DEPLOYMENT_CHECKLIST.md` - This file
- [ ] `README.md` - Updated with new setup instructions

### 22. Team Communication
- [ ] Team notified of deployment
- [ ] Breaking changes documented
- [ ] New features announced
- [ ] Known issues documented

## Rollback Plan

If issues occur:

1. **Immediate Rollback**:
   ```bash
   docker-compose down
   docker-compose up -d --force-recreate --build <previous-version>
   ```

2. **Database Rollback** (if needed):
   ```bash
   docker-compose exec db psql -U f1user f1betting < backup.sql
   ```

3. **Verify**:
   - Check application loads
   - Verify database integrity
   - Test critical functionality

## Support

### Issues to Watch For

1. **CSS not loading**:
   - Check `static/css/output.css` exists
   - Verify `collectstatic` ran successfully
   - Check browser console for 404s

2. **Docker build fails**:
   - Check Node.js dependencies install
   - Verify Tailwind build completes
   - Review build logs

3. **Performance issues**:
   - Check CSS file size
   - Monitor container resources
   - Review database queries

### Emergency Contacts
- [ ] DevOps team contact info documented
- [ ] Database admin contact info documented
- [ ] On-call schedule established

---

## Sign-Off

- [ ] Developer: _______________  Date: __________
- [ ] Reviewer: _______________   Date: __________
- [ ] QA: _______________         Date: __________
- [ ] DevOps: _______________     Date: __________

**Deployment Date**: __________
**Version**: __________
**Git Commit**: __________

---

## Notes

Use this section for deployment-specific notes, issues encountered, or special considerations.

```
[Add notes here]
```
