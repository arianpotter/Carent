from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from CarentApp.models import User,RentalCar,Rent
from rest_framework.decorators import action
from .serializers import UserSerializer,RentSerializer,RentalCarSerializer
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
import datetime,time,calendar
from django.http import Http404
# Create your views here.


class UserView(viewsets.ViewSet):
    def list(self,request):
        if(request.user != AnonymousUser()):
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user,many=False)
            return Response(serializer.data)
        else:
            return Response(status=401)



class RentalCarView(viewsets.ViewSet):

    def list(self,request):
        rentalCars = RentalCar.objects.all()
        serializer = RentalCarSerializer(rentalCars,many=True)
        return Response(serializer.data)

    @action(detail=False)
    def my(self,request):
        if(request.user == AnonymousUser()): return Response(status=401)
        rentalCars = RentalCar.objects.filter(owner__exact=request.user)
        serializer = RentalCarSerializer(rentalCars,many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self,request):
        if(request.user == AnonymousUser()): return Response(status=401)
        params = request.data
        rentalCar = RentalCar(type = params['type'],
        creation_date = datetime.datetime.now(),
        mileage_rate = params['mileage_rate'],
        value = params['value'],
        plate_1 = params['plate_1'],
        plate_2 = params['plate_2'],
        plate_3 = params['plate_3'],
        plate_4 = params['plate_4'],
        color = params['color'],
        owner = request.user,
        rental_time = params['rental_time'],
        rental_daily_rate = params['rental_daily_rate'],
        deposit_amount = params['deposit_amount'],
        city = params['city'],
        delivery_location = params['delivery_location'],
        return_location = params['return_location']
        )
        rentalCar.save()
        return Response(status=201)
    
    @transaction.atomic
    def partial_update(self,request,pk=None):
        if(request.user == AnonymousUser()): return Response(status=401)
        rentalCar = RentalCar.objects.filter(id__exact=pk).first()
        if(rentalCar.owner != request.user): return Response(status=401)
        if(rentalCar == None): raise Http404
        params = request.data
        rentalCar.type = params['type']
        rentalCar.creation_date = datetime.datetime.now()
        rentalCar.mileage_rate = params['mileage_rate']
        rentalCar.value = params['value']
        rentalCar.plate_1 = params['plate_1']
        rentalCar.plate_2 = params['plate_2']
        rentalCar.plate_3 = params['plate_3']
        rentalCar.plate_4 = params['plate_4']
        rentalCar.color = params['color']
        rentalCar.owner = request.user
        rentalCar.rental_time = params['rental_time']
        rentalCar.rental_daily_rate = params['rental_daily_rate']
        rentalCar.deposit_amount = params['deposit_amount']
        rentalCar.city = params['city']
        rentalCar.delivery_location = params['delivery_location']
        rentalCar.return_location = params['return_location']
        rentalCar.save()
        return Response(status=204)





class RentView(viewsets.ViewSet):

    @action(detail=False)
    def my(self,request):
        if(request.user == AnonymousUser()): return Response(status=401)
        if(request.query_params['owner'] == '1'):

            rentalcar = request.query_params['rentalcar']
            rents = Rent.objects.filter(car__owner__exact = request.user).filter(car__id__exact=rentalcar)
            serializer = RentSerializer(rents,many=True)
            return Response(serializer.data)
        else:

            rents = Rent.objects.filter(client__exact=request.user)
            serializer = RentSerializer(rents,many=True)
            return Response(serializer.data)
    
    @transaction.atomic
    def create(self,request):
        if(request.user == AnonymousUser()): return Response(status=401)
        params = request.data
        rent = Rent(car = RentalCar.objects.filter(id__exact=params['car']).first(),
        client = request.user,
        start_date = params['start_date'],
        end_date = params['end_date'],
        desc = params['desc']
        )
        rent.save()
        return Response(status=201)

    @transaction.atomic
    def partial_update(self,request,pk=None):
        if(request.user == AnonymousUser()): return Response(status=401)

        rent = Rent.objects.filter(id__exact=pk).first()
        if(rent == None): raise Http404
        params = request.data
        
        

        rent.rent_status = params['status']

        rent.save()
        return Response(status=204)


