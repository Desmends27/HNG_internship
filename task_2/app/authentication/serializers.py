from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Organization
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class ObtainTokenPair(TokenObtainPairSerializer):
    class Meta:
        model = CustomUser
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        data = super().validate(attrs)
        data["userId"] = self.user.userId
        data["firstName"] = self.user.firstName
        data["lastName"] = self.user.lastName
        data["email"] = self.user.email
        data["phone"] = self.user.phone
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        errors = {}
        if not data.get('firstName'):
            errors['firstName'] = 'First name is required'
        if not data.get('lastName'):
            errors['lastName'] = 'Last name is required'
        if not data.get('email'):
            errors['email'] = 'Email is required'
        if not data.get('password'):
            errors['password'] = 'Password is required'

        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        org_name = f"{user.firstName} Organization"
        organization = Organization.objects.create(name=org_name)
        user.organization.add(organization)
        
        return user
    
    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        
        return instance
    
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["orgId", "name", "description"]
