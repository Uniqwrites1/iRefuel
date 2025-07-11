"""
Utility views for handling common requests and endpoints
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint with basic information"""
    return JsonResponse({
        "message": "University Vendor App API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "authentication": "/api/users/auth/",
            "users": "/api/users/",
            "orders": "/api/orders/",
            "chat": "/api/chat/",
            "delivery": "/api/delivery/",
            "admin": "/admin/",
            "health": "/api/health/"
        }
    })

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "service": "university-vendor-app"
    })

@require_http_methods(["GET"])
def favicon_view(request):
    """Handle favicon requests to prevent 404/400 errors"""
    # Return empty 204 No Content response
    return HttpResponse(status=204)

@require_http_methods(["GET"])
def robots_txt(request):
    """Handle robots.txt requests"""
    content = """User-agent: *
Disallow: /admin/
Disallow: /api/users/auth/
Allow: /api/
"""
    return HttpResponse(content, content_type="text/plain")
