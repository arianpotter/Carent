from django.contrib import admin
from .models import User,RentalCar,Rent

# Register your models here.
admin.site.register(User)
admin.site.register(RentalCar)
admin.site.register(Rent)