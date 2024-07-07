from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TokenObtainPairSerializer, RegistrationSerializer, OrganizationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .models import Organization

# Create your views here.


class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': access_token,
                    'user': {
                        'userId': str(user.userId),
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Register(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "status": "success",
                "message": "Registration successful",
                'data': {
                    'accessToken': access_token,
                    'user': {
                        'userId': str(user.userId),
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(userId=id)
        except CustomUser.DoesNotExist:
            return Response({
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "status": "success",
                "message": "Successful",
                "data": {
                    'userId': str(user.userId),
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'phone': user.phone
                }
            }
        )


class OrganisationListView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            organizations = user.organization.all()
            serializer = OrganizationSerializer(organizations, many=True)

            return Response(
                {
                    "status": "success",
                    "message": "Organisation created successfully",
                    "data": serializer.data
                }
            )
        else:
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Organisation created successfully",
                    "data": serializer.data
                }
            )

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            organization = Organization.objects.create(**request.data)
            user.organization.add(organization)
            serializer = OrganizationSerializer(organization)
            return Response({
                'status': 'success',
                'message': 'Organisations fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                }
            )

class AddUserToOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId, *args, **kwargs):
        try:
            organization = Organization.objects.get(orgId=orgId)
        except Organization.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": f"Organization with ID {orgId} does not exist",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        userId = request.data.get('userId')
        
        try:
            user = CustomUser.objects.get(userId=userId)
        except CustomUser.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": f"User with ID {userId} does not exist",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        organization.users.add(user)

        return Response({
            "status": "success",
            "message": "User added to organization successfully"
        }, status=status.HTTP_200_OK)