# Render Environment Variables Setup

## Essential Environment Variables

After your Render deployment starts, you need to set these environment variables in your Render Dashboard:

### 1. Navigate to Your Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your web service
3. Go to the "Environment" tab

### 2. Add These Required Variables

#### Django Core Settings
```
SECRET_KEY=your-super-secret-production-key-change-this-to-random-50-character-string
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

#### CORS Settings (for Flutter/Mobile)
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
```

#### Superuser Creation (Important!)
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=SecureAdminPassword123!
```

### 3. Database Configuration
**Render automatically provides `DATABASE_URL`** when you connect a PostgreSQL database to your service. You don't need to set individual database variables.

If you haven't created a PostgreSQL database yet:
1. In Render Dashboard, go to "New" → "PostgreSQL"
2. Create the database
3. Connect it to your web service
4. Render will automatically set `DATABASE_URL`

### 4. Optional Variables (Set as needed)

#### Security Headers
```
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

#### JWT Settings (optional - defaults are fine)
```
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
```

#### Redis (if using WebSocket chat)
```
REDIS_URL=redis://your-redis-url:6379
USE_REDIS=True
```

## Post-Deployment Steps

### 1. Create Superuser Automatically
After setting the superuser environment variables above, the system will automatically create an admin user when the service starts.

### 2. Verify Deployment
Once deployed, your API will be available at:
```
https://your-app-name.onrender.com/api/
```

### 3. Test Admin Access
Visit the admin panel:
```
https://your-app-name.onrender.com/admin/
```

Login with the credentials you set in the environment variables.

### 4. Test API Endpoints
Test key endpoints:
- Health check: `GET /api/health/`
- User registration: `POST /api/users/register/`
- Login: `POST /api/users/login/`

## Environment Variables Template

Copy this to your Render Dashboard Environment tab:

```
SECRET_KEY=django-insecure-change-this-to-a-real-secret-key-50-characters-long-random-string
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

## Troubleshooting

### If deployment fails:
1. Check Render build logs for specific errors
2. Verify all required environment variables are set
3. Ensure PostgreSQL database is connected
4. Check that `DATABASE_URL` is automatically provided by Render

### If superuser isn't created:
1. Verify the superuser environment variables are set correctly
2. Check the deployment logs for any creation errors
3. The superuser is created during the build process

### Common Issues:
- **Database connection errors**: Ensure PostgreSQL database is connected to your service
- **Static files not loading**: Whitenoise is configured, static files should work automatically
- **CORS errors from Flutter**: Update `CORS_ALLOWED_ORIGINS` with your Flutter app's domains

## Security Notes

1. **SECRET_KEY**: Generate a new random 50-character string for production
2. **Superuser Password**: Use a strong password with mixed case, numbers, and symbols
3. **CORS Origins**: Only include domains that should access your API
4. **HTTPS**: Render provides SSL certificates automatically

## Next Steps

After successful deployment:
1. Update your Flutter app to use the production API URL
2. Test all API endpoints with your frontend
3. Set up monitoring and logging as needed
4. Configure any additional services (Redis for WebSocket, email providers, etc.)
