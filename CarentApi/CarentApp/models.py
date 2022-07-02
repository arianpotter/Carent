from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class RentalCar(models.Model):
    type = models.CharField(max_length=50)
    creation_date = models.DateTimeField('creation date')
    mileage_rate = models.BigIntegerField()
    value = models.FloatField()
    plate_1 = models.CharField(max_length=50)
    plate_2 = models.CharField(max_length=50)
    plate_3 = models.CharField(max_length=50)
    plate_4 = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    owner = models.ForeignKey('User',on_delete=models.CASCADE)
    rental_time = models.IntegerField()
    rental_daily_rate = models.FloatField()
    deposit_amount = models.FloatField()
    city = models.CharField(max_length=50)
    delivery_location = models.CharField(max_length=50)
    return_location = models.CharField(max_length=50)


class Rent(models.Model):
    car = models.ForeignKey('RentalCar',on_delete=models.CASCADE)
    client = models.ForeignKey('User',on_delete=models.CASCADE)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    desc = models.CharField(max_length=200)
    status_choices = [
        ('R','Request'),
        ('I','In Rent'),
        ('E','Expired'),
        ('D','Denied'),
        ('P','Pending')
    ]
    rent_status = models.CharField(
        max_length=2,
        choices = status_choices,
        default = 'R'
    )


    
