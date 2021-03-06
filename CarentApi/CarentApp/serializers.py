from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from .models import User,RentalCar,Rent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user


class RentalCarSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = RentalCar
        fields = '__all__'
        depth = 1

class RentSerializer(serializers.ModelSerializer):
    car = RentalCarSerializer()
    client = UserSerializer()
    class Meta:
        model = Rent
        fields = '__all__'
        depth = 2