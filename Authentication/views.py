from django.shortcuts import render
from rest_framework.views import APIView
from Authentication.serializers import *
from Authentication.models import UserRegistration
from rest_framework import status
from rest_framework.response import Response
from helper.Generate_jwt import get_tokens_for_user
from helper.Hide import custom_hasher
from helper.email_regex import validate_email

# Create your views here.

class UserRegisterView(APIView) :
    def post(self,request) :
        try :
            # Custom validation to ensure all fields are present                
            email = request.data.get('email').lower()
            if not email:
                return Response({'status': False, 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            else :
                if validate_email(email):
                    pass
                else:
                    return Response({'status': False, 'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid() :
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                profile_image = serializer.validated_data.get('profile_image')
                
                # Manual field validation
                if not username:
                    return Response({'status': False, 'message': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not password:
                    return Response({'status': False, 'message': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

                if not profile_image:
                    return Response({'status': False, 'message': 'Profile image is required'}, status=status.HTTP_400_BAD_REQUEST)
                # Check if email exists in the database
                try:
                    user = UserRegistration.objects.get(email=email)
                    # If user already exists, return response indicating the user already exists
                    return Response({'status': False, 'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                except UserRegistration.DoesNotExist:
                    
                    user = UserRegistration.objects.create(
                        username=username,
                        email=email,
                        password = custom_hasher(password),
                        profile_image = profile_image
                    )
                    if user:
                        # token = get_tokens_for_user(user)
                        return Response({'status': True, 'message': 'User created successfully',}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'status': False, 'message': 'Failed to create user'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Handle case where serializer is invalid
                errors = serializer.errors
                return Response({'status': False, 'message': 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   
         
class UserLoginView(APIView) :
    def post(self,request) :
        try:
            email = request.data.get('email').lower()
            password = request.data.get('password')
            password = custom_hasher(password)
            # Check if both email and password are provided
            if not email or not password:
                return Response({'status': False, 'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
            # Check if a user with the provided email exists
            try:
                user = UserRegistration.objects.get(email=email)
                # Verify the password
                if user.password == password :
                    token = get_tokens_for_user(user)
                    return Response({'status': True, 'message': 'Login successful.', 'token' : token['access']}, status=status.HTTP_200_OK)
                else:
                    # Passwords do not match
                    return Response({'status': False, 'message': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
            except UserRegistration.DoesNotExist:
                return Response({'status': False, 'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)      
        
