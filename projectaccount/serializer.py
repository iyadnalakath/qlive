from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from urllib.parse import urljoin



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class LogoutSerializer(serializers.Serializer):
    pass




class RegisterStaffSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = Account
        fields = ["full_name", "username", "email", "phone", "password", "password2"]

        read_only_fields = ("password2",)

        extra_kwargs = {
            "password": {"write_only": True},
            # 'password2':{'write_only':True}
        }


    def create(self, validated_data):
        password = self.validated_data["password"]


        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user = Account.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                full_name=self.validated_data["full_name"],
                phone=self.validated_data["phone"],
            )
            user.set_password(validated_data["password"])
            user.role = "staff"
            user.save()
            return user

class UpdateStaffPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "is_staff",
            "is_admin",
            "is_active",
            "full_name",
            "role",
            "email",
            "is_staff",
            "phone",
        )