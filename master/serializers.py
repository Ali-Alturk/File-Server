# master/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 'is_staff', 'created_at')

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Create User instance
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data.get('is_staff', False)
        )
        user.set_password(password)
        user.save()

        # Create UserProfile instance
        user_profile = UserProfile.objects.create(
            user=user,
            username=validated_data['username'],
            email=validated_data['email'],
            stored_password=user.password,  # Store the hashed password
            is_staff=validated_data.get('is_staff', False),
        )
        return user_profile

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.user.set_password(password)
            instance.stored_password = instance.user.password
            instance.user.save()

        # Update both User and UserProfile
        for attr, value in validated_data.items():
            setattr(instance.user, attr, value)  # Update User model
            setattr(instance, attr, value)  # Update UserProfile model

        instance.user.save()
        instance.save()
        return instance