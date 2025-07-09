# Render Deployment Checklist

## Pre-deployment Preparation

### ✅ Code Preparation
- [ ] Code pushed to GitHub repository
- [ ] `requirements.txt` updated with production dependencies
- [ ] `render-build.sh` script created and executable
- [ ] WhiteNoise middleware added to settings
- [ ] Production security settings configured

### ✅ Environment Configuration
- [ ] `.env.production` template reviewed
- [ ] Production SECRET_KEY generated
- [ ] Frontend domain identified for CORS

## Render Setup

### ✅ Database Setup
- [ ] PostgreSQL database created on Render
- [ ] Database connection details copied
- [ ] Database environment variables noted

### ✅ Web Service Setup
- [ ] Web service created and connected to GitHub
- [ ] Build command set: `./render-build.sh`
- [ ] Start command set: `gunicorn irefuel_backend.wsgi:application`
- [ ] Environment variables configured

## Environment Variables Checklist

### ✅ Required Variables
- [ ] `SECRET_KEY` - Strong, unique production key
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` - Your Render app domain
- [ ] `USE_POSTGRES=True`
- [ ] `DB_NAME` - From Render PostgreSQL
- [ ] `DB_USER` - From Render PostgreSQL
- [ ] `DB_PASSWORD` - From Render PostgreSQL
- [ ] `DB_HOST` - From Render PostgreSQL
- [ ] `DB_PORT=5432`

### ✅ CORS Configuration
- [ ] `CORS_ALLOW_ALL_ORIGINS=False`
- [ ] `CORS_ALLOWED_ORIGINS` - Your frontend URL

### ✅ Security Settings
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SECURE_BROWSER_XSS_FILTER=True`
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF=True`
- [ ] `X_FRAME_OPTIONS=DENY`
- [ ] `SECURE_HSTS_SECONDS=31536000`

## Post-deployment

### ✅ Database Migration
- [ ] Access Render shell
- [ ] Run `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### ✅ Testing
- [ ] API endpoints accessible
- [ ] Admin panel working
- [ ] Database operations functional
- [ ] Authentication working
- [ ] CORS configured correctly

### ✅ Frontend Integration
- [ ] Update frontend API_BASE_URL
- [ ] Test authentication flow
- [ ] Test core functionality
- [ ] Verify real-time features

## Quick Commands

### Generate SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Test Database Connection
```bash
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Database connected!')"
```

### Check Deployment
```bash
curl https://your-app-name.onrender.com/api/users/cafeterias/
```

## Troubleshooting

### Common Issues
- [ ] Build fails: Check `render-build.sh` permissions
- [ ] 500 errors: Check environment variables
- [ ] Static files not loading: Verify WhiteNoise configuration
- [ ] Database errors: Check connection details
- [ ] CORS errors: Update allowed origins

### Useful Commands
```bash
# View logs
# Go to Render dashboard > Your service > Logs

# Access shell
# Go to Render dashboard > Your service > Shell

# Check migrations
python manage.py showmigrations

# Collect static files manually
python manage.py collectstatic --noinput
```

## Production URLs

After deployment, your API will be available at:
- **API Base**: `https://your-app-name.onrender.com/api/`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`
- **WebSocket**: `wss://your-app-name.onrender.com/ws/`

## Success Criteria

### ✅ Deployment Successful When:
- [ ] Web service shows "Live" status
- [ ] API endpoints return expected responses
- [ ] Admin panel accessible
- [ ] Database operations work
- [ ] Authentication flow functional
- [ ] No critical errors in logs

Your University Vendor App is ready for production! 🚀
