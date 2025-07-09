# Step-by-Step Render Deployment Guide

## Overview
This guide will walk you through deploying your University Vendor App to Render step by step.

## Step 1: Prepare Your Repository

### 1.1 Commit All Changes
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 1.2 Verify Files
Ensure these files are in your repository:
- `render-build.sh` - Build script
- `requirements.txt` - Updated with gunicorn and whitenoise
- `runtime.txt` - Python version specification
- `.env.production` - Template for production variables

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

## Step 3: Create PostgreSQL Database

### 3.1 Create Database
1. In Render Dashboard, click "New" → "PostgreSQL"
2. Configure database:
   - **Name**: `irefuel-db`
   - **Database**: `irefuel_db`
   - **User**: `irefuel_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (for testing) or paid for production

### 3.2 Get Connection Details
After creation, copy these details:
- **Hostname**: `dpg-xxxxx-a.oregon-postgres.render.com`
- **Port**: `5432`
- **Database**: `irefuel_db`
- **Username**: `irefuel_user`
- **Password**: `[auto-generated]`

## Step 4: Create Web Service

### 4.1 Create Service
1. In Render Dashboard, click "New" → "Web Service"
2. Connect your GitHub repository
3. Select your `iRefuel` repository

### 4.2 Configure Service
- **Name**: `irefuel-backend`
- **Environment**: `Python 3`
- **Region**: Same as your database
- **Branch**: `main`
- **Build Command**: `./render-build.sh`
- **Start Command**: `gunicorn irefuel_backend.wsgi:application`
- **Plan**: Free (for testing) or paid for production

## Step 5: Set Environment Variables

In the web service settings, add these environment variables:

### Required Variables:
```
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=irefuel-backend.onrender.com
USE_POSTGRES=True
DB_NAME=irefuel_db
DB_USER=irefuel_user
DB_PASSWORD=[your-database-password]
DB_HOST=[your-database-host]
DB_PORT=5432
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
USE_REDIS=False
MEDIA_URL=/media/
STATIC_URL=/static/
DRF_PAGE_SIZE=20
LOG_LEVEL=INFO
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Generate SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 6: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Run the build script
   - Install dependencies
   - Collect static files
   - Start your application

## Step 7: Run Database Migrations

### 7.1 Access Shell
1. Go to your web service in Render
2. Click "Shell" tab
3. Wait for shell to connect

### 7.2 Run Migrations
```bash
python manage.py migrate
```

### 7.3 Create Superuser
```bash
python manage.py createsuperuser
```

## Step 8: Test Your Deployment

### 8.1 Check Service Status
- Service should show "Live" status
- No critical errors in logs

### 8.2 Test API Endpoints
```bash
# Test public endpoint
curl https://irefuel-backend.onrender.com/api/users/cafeterias/

# Should return: {"detail":"Authentication credentials were not provided."}
```

### 8.3 Test Admin Panel
Visit: `https://irefuel-backend.onrender.com/admin/`

## Step 9: Update Frontend Configuration

Update your frontend to use the production API:

```javascript
const API_BASE_URL = 'https://irefuel-backend.onrender.com/api/';
const WS_BASE_URL = 'wss://irefuel-backend.onrender.com/ws/';
```

## Step 10: Final Testing

### 10.1 Test Authentication
```bash
# Register a test user
curl -X POST https://irefuel-backend.onrender.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password_confirm":"testpass123","first_name":"Test","last_name":"User","user_type":"student","phone_number":"1234567890","campus_location":"Test Campus"}'
```

### 10.2 Test Login
```bash
# Login with test user
curl -X POST https://irefuel-backend.onrender.com/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## Troubleshooting

### Common Issues:

#### Build Fails
- Check logs for specific error
- Verify `render-build.sh` is in root directory
- Ensure all dependencies in `requirements.txt`

#### 500 Internal Server Error
- Check environment variables
- Verify SECRET_KEY is set
- Check database connection

#### Static Files Not Loading
- Verify WhiteNoise is in MIDDLEWARE
- Check STATIC_ROOT and STATIC_URL settings

#### Database Connection Error
- Verify database credentials
- Check if database is running
- Ensure USE_POSTGRES=True

### Useful Commands:
```bash
# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Connected!')"

# View migration status
python manage.py showmigrations

# Collect static files manually
python manage.py collectstatic --noinput
```

## Success!

Your University Vendor App is now live at:
- **API**: `https://irefuel-backend.onrender.com/api/`
- **Admin**: `https://irefuel-backend.onrender.com/admin/`
- **WebSocket**: `wss://irefuel-backend.onrender.com/ws/`

## Next Steps

1. **Set up monitoring** - Monitor logs and performance
2. **Configure custom domain** - Use your own domain name
3. **Set up backups** - Regular database backups
4. **Update frontend** - Point frontend to production API
5. **Load testing** - Test with expected traffic

Congratulations! Your University Vendor App is now live in production! 🎉

## Support

If you encounter issues:
1. Check Render service logs
2. Review deployment checklist
3. Test with Postman collection
4. Check database connectivity
5. Verify environment variables
