from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

from account import models

# Create your views here.
class Signup(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors)


# class Login(viewsets.ViewSet):
"""This class handle login functionality
    login only  with username and password """
#     permission_classes = [AllowAny]

#     def create(self, request):
#         username = request.data.get("username")
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(
#                 {"error": "Username and password are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user = authenticate(username=username, password=password)

#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response(
#                 {"token": token.key, "message": "Login successful."},
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             {"error": "Invalid credentials."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )

    
class Login(viewsets.ViewSet):
    """This class handle login functionality
    login with username and password or email and password"""
    permission_classes = [AllowAny]

    def create(self, request):
        # email = request.data.get("email")
        username_or_email = request.data.get("username")
        password = request.data.get("password")
    

    

    
        # password = request.data.get('password')
        # user = authenticate(username=username_or_email, password=password)

        # if not password:
        #     return Response(
        #         {"error": "Password is required."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        # if not (email or username):
        #     return Response(
        #         {"error": "Either email or username is required."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        
        ##use two query to check username and email

        # user = authenticate(username=username or email, password=password)
        # if username:
        #     user = authenticate(username=username, password=password)

        # elif email:
        #     try:
        #         user_obj = User.objects.get(email=email)
        #         user = authenticate(username=user_obj.username, password=password)
        #     except User.DoesNotExist:
        #         user = None

        ##use single query to check username and email
        user_query = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
        user = None
        if user_query:
            user = authenticate(username=user_query.username, password=password)
            


        # user = authenticate(username=username, password=password)
##Authenticate with email or username
        # username_or_email = request.data.get('username_or_email')
        # password = request.data.get('password')
        # if not username_or_email or not password:
        #     return Response({"detail": "Username or email and password required."}, status=status.HTTP_400_BAD_REQUEST)

        
        # user = None
        # if '@' in username_or_email:
        #     try:
        #         user = User.objects.get(email=username_or_email)
        #     except User.DoesNotExist:
        #         return Response({"detail": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        # else:  
        #     try:
        #         user = User.objects.get(username=username_or_email)
        #     except User.DoesNotExist:
        #         return Response({"detail": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

       
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response(
                    {
                        "token": token.key,
                        "message": "Login successful.",
                        
                        "user_data":serializer.data,
                        
                    },
                    status=status.HTTP_200_OK,
                )
            # return Response(
            #     {"token": token.key, "message": "Login successful."   },



            #     status=status.HTTP_200_OK,
            # )
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class Logout(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def create(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})
    
