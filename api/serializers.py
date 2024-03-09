from rest_framework import serializers
from main.models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'phone_number',
            'state', 'lga',
            'gender', 'date_joined', 'password'
        ]
        
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'phone_number',
            'state', 'lga',
            'gender', 'password'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        

