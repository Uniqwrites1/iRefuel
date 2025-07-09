from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Cafeteria, MenuItem
from .serializers import (
    UserRegistrationSerializer, UserSerializer, LoginSerializer,
    CafeteriaSerializer, MenuItemSerializer, MenuItemListSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CafeteriaListView(generics.ListAPIView):
    queryset = Cafeteria.objects.filter(is_active=True)
    serializer_class = CafeteriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CafeteriaDetailView(generics.RetrieveAPIView):
    queryset = Cafeteria.objects.filter(is_active=True)
    serializer_class = CafeteriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CafeteriaMenuView(generics.ListAPIView):
    serializer_class = MenuItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cafeteria_id = self.kwargs['cafeteria_id']
        return MenuItem.objects.filter(
            cafeteria_id=cafeteria_id, 
            is_available=True,
            cafeteria__is_active=True
        )


# Vendor-specific views
class VendorCafeteriaView(generics.RetrieveUpdateAPIView):
    serializer_class = CafeteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.user_type != 'vendor':
            raise PermissionDenied("Only vendors can access this.")
        return Cafeteria.objects.get(vendor=self.request.user)


class VendorMenuItemsView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'vendor':
            raise PermissionDenied("Only vendors can access this.")
        cafeteria = Cafeteria.objects.get(vendor=self.request.user)
        return MenuItem.objects.filter(cafeteria=cafeteria)

    def perform_create(self, serializer):
        if self.request.user.user_type != 'vendor':
            raise PermissionDenied("Only vendors can create menu items.")
        try:
            cafeteria = Cafeteria.objects.get(vendor=self.request.user)
            serializer.save(cafeteria=cafeteria)
        except Cafeteria.DoesNotExist:
            raise PermissionDenied("Vendor must have a cafeteria to create menu items.")


class VendorMenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'vendor':
            raise PermissionDenied("Only vendors can access this.")
        cafeteria = Cafeteria.objects.get(vendor=self.request.user)
        return MenuItem.objects.filter(cafeteria=cafeteria)
