
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# here we define the serializer for our custom user model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    # this serializer is used for user registration

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    # this method validates that the passwords match and fullname has both first and last name

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if " " not in data['fullname'].strip():
            raise serializers.ValidationError({"fullname": "Fullname has to consist of first and last name."})
        return data

    # this method creates a new user and associated auth token

    def create(self, validated_data):
        validated_data.pop('repeated_password')

        user = User(
            email=validated_data['email'],
            fullname=validated_data['fullname']
        )
    
    # set the user's password securely

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        return user
