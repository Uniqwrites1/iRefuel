from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Cafeteria, MenuItem

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'user_type', 'phone_number', 'campus_location')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'user_type', 'phone_number', 'campus_location', 'profile_picture',
                 'is_available', 'created_at')
        read_only_fields = ('id', 'created_at')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        return attrs


class CafeteriaSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
    
    class Meta:
        model = Cafeteria
        fields = ('id', 'name', 'description', 'vendor', 'vendor_name', 'location', 
                 'phone_number', 'opening_time', 'closing_time', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class MenuItemSerializer(serializers.ModelSerializer):
    cafeteria_name = serializers.CharField(source='cafeteria.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ('id', 'cafeteria', 'cafeteria_name', 'name', 'description', 
                 'price', 'category', 'image', 'is_available', 'preparation_time', 'created_at')
        read_only_fields = ('id', 'cafeteria', 'created_at')


class MenuItemListSerializer(serializers.ModelSerializer):
    """Simplified serializer for menu listing"""
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'price', 'category', 'image', 'is_available', 'preparation_time')
