from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from main.models import *

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('phone_number', )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, required=False)
    address = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'profile', 'address')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }


    def create(self, validated_data):
        return User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Validated data is not available to authenticate')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



