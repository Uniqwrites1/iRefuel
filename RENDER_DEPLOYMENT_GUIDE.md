# Render Deployment Guide

## Overview
This guide will help you deploy the University Vendor App backend to Render, a modern cloud platform that makes deployment simple.

## Prerequisites
1. Render account (sign up at https://render.com)
2. GitHub repository with your code
3. PostgreSQL database (Render provides this)

## Step 1: Prepare Your Code for Production

### 1.1 Update requirements.txt
Ensure all dependencies are listed:
```
gunicorn==21.2.0
whitenoise==6.6.0
```

### 1.2 Create Production Settings
Your current settings.py already uses environment variables, which is perfect for Render.

### 1.3 Static Files Configuration
Render needs proper static file handling (already configured in your settings.py).

## Step 2: Create Render Configuration Files

### 2.1 Build Script (render-build.sh)
This script runs during deployment to install dependencies and collect static files.

### 2.2 Start Command
Render will use gunicorn to serve your Django app.

## Step 3: Environment Variables for Render

Set these environment variables in Render dashboard:

### Required Variables:
```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
USE_POSTGRES=True
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ALLOW_ALL_ORIGINS=False
```

### Optional Variables:
```
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
USE_REDIS=False
MEDIA_URL=/media/
STATIC_URL=/static/
DRF_PAGE_SIZE=20
LOG_LEVEL=INFO
```

## Step 4: Deploy to Render

### 4.1 Create PostgreSQL Database
1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Choose a name (e.g., "irefuel-db")
4. Select region closest to your users
5. Copy the connection details

### 4.2 Create Web Service
1. Go to Render Dashboard
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: irefuel-backend
   - **Environment**: Python 3
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `gunicorn irefuel_backend.wsgi:application`
   - **Instance Type**: Free (or paid for better performance)

### 4.3 Set Environment Variables
In the Render dashboard, add all the environment variables listed above.

## Step 5: Database Migration

After deployment, run migrations:
1. Go to your web service in Render
2. Click "Shell" tab
3. Run: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`

## Step 6: Test Your Deployment

### API Base URL
Your API will be available at:
```
https://your-app-name.onrender.com/api/
```

### Admin Panel
```
https://your-app-name.onrender.com/admin/
```

## Step 7: Configure Frontend

Update your frontend to use the production API URL:
```javascript
const API_BASE_URL = 'https://your-app-name.onrender.com/api/';
```

## Step 8: SSL and Security

Render automatically provides SSL certificates. Update your settings for production:

### Security Headers
Already configured in your settings.py with environment variables.

## Troubleshooting

### Common Issues:

1. **Static Files Not Loading**
   - Ensure `whitenoise` is in MIDDLEWARE
   - Check `STATIC_ROOT` and `STATIC_URL` settings

2. **Database Connection Errors**
   - Verify database environment variables
   - Check database host/port/credentials

3. **CORS Issues**
   - Update `CORS_ALLOWED_ORIGINS` with your frontend URL
   - Set `CORS_ALLOW_ALL_ORIGINS=False` in production

4. **Environment Variables Not Working**
   - Double-check variable names in Render dashboard
   - Restart the service after adding variables

### Logs
Check logs in Render dashboard under "Logs" tab for debugging.

## Performance Optimization

### For Better Performance:
1. Upgrade to paid Render plan
2. Enable Redis for caching and sessions
3. Use CDN for static files
4. Optimize database queries

### Monitoring
- Use Render's built-in monitoring
- Set up error tracking (Sentry)
- Monitor database performance

## Backup Strategy

### Database Backups
1. Render PostgreSQL includes automated backups
2. Set up additional backup schedule if needed

### Code Backups
- Your code is backed up in GitHub
- Tag releases for easy rollbacks

## Scaling

### Auto-scaling
- Render can auto-scale based on traffic
- Configure in service settings

### Database Scaling
- Upgrade PostgreSQL plan as needed
- Monitor database performance

## Cost Considerations

### Free Tier Limitations:
- Service sleeps after 15 minutes of inactivity
- 750 hours per month limit
- Basic database size

### Paid Plans:
- Always-on services
- Better performance
- More database storage
- Priority support

## Security Best Practices

### Environment Variables
- Never commit secrets to GitHub
- Use strong, unique SECRET_KEY
- Rotate database passwords regularly

### Django Security
- Keep Django updated
- Use HTTPS only
- Enable security middleware

## Maintenance

### Regular Tasks:
1. Monitor application logs
2. Update dependencies
3. Review database performance
4. Check error rates

### Updates:
1. Push to GitHub
2. Render auto-deploys from main branch
3. Monitor deployment logs

## Support Resources

### Render Documentation:
- https://render.com/docs
- Django deployment guide
- PostgreSQL setup

### Django Production:
- Django deployment checklist
- Security considerations
- Performance tuning

---

Your University Vendor App is now ready for production deployment on Render! 🚀
