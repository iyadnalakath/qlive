from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    LoginSerializer,
    RegisterStaffSerializer,
    UserListSerializer,
    UpdateStaffPasswordSerializer
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from django.http import Http404




class RegisterUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if request.user.role != 'admin':
            return Response({'error': 'You do not have permission to view users.'}, status=status.HTTP_403_FORBIDDEN)

       
        if pk is not None:
            try:
                user = self.get_object(pk)
                serializer = UserListSerializer(user)
                return Response(serializer.data)
            except Http404:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        users = Account.objects.filter(role='staff')
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'You do not have permission to create a user with admin role.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RegisterStaffSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data["email"] = account.email
            data["username"] = account.username
            data["pk"] = account.pk
            data["response"] = "successfully registered new user."

            token = Token.objects.get(user=account).key
            data["token"] = token

            status_code = status.HTTP_200_OK
            return Response(data, status=status_code)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
class UpdateStaffPasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateStaffPasswordSerializer

    def get_object(self, pk):
        try:
            staff_member = Account.objects.get(pk=pk)
            if self.request.user.role != 'admin':
                if staff_member != self.request.user:
                    raise PermissionDenied("You do not have permission to update this user's password.")
            return staff_member
        except Account.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        if pk is not None:
            staff_member = self.get_object(pk)
            serializer = UpdateStaffPasswordSerializer(staff_member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'Password updated successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User ID (pk) is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            user = serializer.validated_data

            username = request.data.get("username")
            password = request.data.get("password")
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            context["response"] = "Successfully authenticated."
            context["pk"] = user.pk
            context["username"] = username.lower()
            context["token"] = token.key
            context["role"] = user.role
            context["response"] = "Successfully authenticated."
            return Response(context, status=status.HTTP_200_OK)
        else:
            context["response"] = "Error"
            context["error_message"] = "The username or password is incorrect"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            request.user.auth_token.delete()
            context["response"] = "LogOut Successful."
            status_code = status.HTTP_200_OK
        except:
            context["response"] = "Error"
            context["error_message"] = "Invalid Token"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(context, status=status_code)