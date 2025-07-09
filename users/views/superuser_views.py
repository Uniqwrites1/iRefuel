from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from decouple import config

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def create_superuser_api(request):
    """
    One-time API endpoint to create superuser.
    Remove this endpoint after creating superuser for security.
    """
    # Security check - only allow if no superuser exists
    if User.objects.filter(is_superuser=True).exists():
        return Response(
            {'error': 'Superuser already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get data from request or use defaults
    username = request.data.get('username', 'admin')
    email = request.data.get('email', 'admin@irefuel.com')
    password = request.data.get('password', 'admin123')
    
    # Additional security check
    secret_key = request.data.get('secret_key')
    if secret_key != config('SUPERUSER_SECRET_KEY', default='create-superuser-2025'):
        return Response(
            {'error': 'Invalid secret key'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type='vendor'
        )
        
        return Response({
            'message': 'Superuser created successfully',
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
