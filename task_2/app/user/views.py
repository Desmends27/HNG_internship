from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, UserDetailSerializer, OrganisationSerializer
from .models import CustomUser, Organisation
from rest_framework.permissions import IsAuthenticated


class Login(TokenObtainPairView):
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
                        'userId': str(user.id),  # Ensure it's a string
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


class Register(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': access_token,
                    'user': {
                        'userId': str(user.id),
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                    }
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "errors": serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(userId=user_id)
            print(user)
        except CustomUser.DoesNotExist:
            return Response({
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_404_NOT_FOUND)

        user_organisations = Organisation.objects.filter(users=user)
        requesting_user = request.user

        # Check if the requesting user has permission to view the user's details
        if user == requesting_user or user_organisations.filter(users=requesting_user).exists() or user_organisations.filter(created_by=requesting_user).exists():
            serializer = UserDetailSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User details fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_403_FORBIDDEN)

class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        organisations = Organisation.objects.filter(created_by=user)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            'status': 'success',
            'message': 'Organisations fetched successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=pk, created_by=request.user)
        except Organisation.DoesNotExist:
            return Response({'status': 'error', 'message': 'Organisation not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganisationSerializer(organisation)
        return Response({
            'status': 'success',
            'message': 'Organisation details fetched successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class OrganisationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'Bad Request',
                'message': 'Client error',
                'statusCode': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class OrganisationAddUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=pk, created_by=request.user)
        except Organisation.DoesNotExist:
            return Response({'status': 'error', 'message': 'Organisation not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('userId')
        return Response({
            'status': 'success',
            'message': 'User added to organisation successfully'
        }, status=status.HTTP_200_OK)