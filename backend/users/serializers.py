from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be returned
            'profile_photo': {'required': False},  # Avatar is optional
        }

    def create(self, validated_data):
        # Create user and hash the password
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Handle password hashing on update
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
