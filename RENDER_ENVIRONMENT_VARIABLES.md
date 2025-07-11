# Render Environment Variables Configuration

## Required Environment Variables for Render Deployment

Set these environment variables in your Render dashboard under your web service settings:

### Django Core Settings
```
SECRET_KEY=django-insecure-6nb8nug(k&+)!xuaxf*0ys2tliqa67pz*38&5ds4=s4t9511tx
DEBUG=False
ALLOWED_HOSTS=irefuel.onrender.com
```

### Database Configuration (PostgreSQL)
```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```
**Note:** Render will automatically provide the `DATABASE_URL` when you add a PostgreSQL database. Use that exact value.

### JWT Configuration
```
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
```

### CORS Configuration (for Flutter/Mobile)
```
CORS_ALLOW_ALL_ORIGINS=True
```

### Superuser Auto-Creation
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@irefuel.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### Media Files (Optional)
```
USE_S3=False
```

## Setting Environment Variables on Render

1. Go to your Render dashboard
2. Select your web service (irefuel)
3. Go to "Environment" tab
4. Add each variable with its value
5. Click "Save Changes"
6. Render will automatically redeploy your service

## Important Notes

- **SECRET_KEY**: Change this to a secure random key for production
- **DEBUG**: Always set to `False` in production
- **ALLOWED_HOSTS**: Must include your Render domain (`irefuel.onrender.com`)
- **DATABASE_URL**: Use the exact URL provided by Render's PostgreSQL service
- **CORS**: Set to `True` for mobile app integration (restrict in production if needed)

## Current Status

The deployment is successful but needs the `ALLOWED_HOSTS` environment variable updated to include `irefuel.onrender.com`.

After updating this variable, the app should be fully functional at:
- **API Base URL**: `https://irefuel.onrender.com/api/`
- **Admin Panel**: `https://irefuel.onrender.com/admin/`
