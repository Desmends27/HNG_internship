from rest_framework import serializers
from .models import CustomUser, Organisation
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', 'password']

    def validate(self, data):
        errors = []
        if not data.get('firstName'):
            errors.append({'field': 'firstName', 'message': 'First name is required'})
        if not data.get('lastName'):
            errors.append({'field': 'lastName', 'message': 'Last name is required'})
        if not data.get('email'):
            errors.append({'field': 'email', 'message': 'Email is required'})
        if not data.get('password'):
            errors.append({'field': 'password', 'message': 'Password is required'})
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        organisation_name = f"{validated_data['firstName']}'s Organisation"
        org = Organisation.objects.create(
            name=organisation_name, created_by=user)
        org.save()
        return user
    
    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', ]

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description', 'created_by']