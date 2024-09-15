from django.shortcuts import render

# Create your views here.
# inventory_app/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from apps.user.models import Role, User
from apps.user.utilities.utills import get_tokens_for_user
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.viewsets import ViewSet
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
class LoginApi(ViewSet):
    authentication_classes = [] 

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()
            if not user or not user.check_password(password):
                return Response(
                    {
                        "message": "Invalid Email / Password",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user is active
            if not user.is_active:
                return Response(
                    {
                        "message": "Your account is currently inactive so you can't login.",
                        "status": status.HTTP_423_LOCKED,
                    },
                    status=status.HTTP_423_LOCKED,
                )

            # Authenticate user
            user = authenticate(email=email, password=password)
            if user:
                # Generate JWT token
                token = get_tokens_for_user(user)
                response = {
                    "message": "Login successful",
                    "token": token,
                    "status": status.HTTP_200_OK,
                }
                return Response(response, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterViewset(viewsets.ModelViewSet):
    
    authentication_classes = []
    
    def create(self, request):
        print("request.data",request.data)
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            response = {
                "message": "User created successfully",
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "message": serializer.errors.get(next(iter(serializer.errors)))[0],
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)