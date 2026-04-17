from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
import datetime



# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guest =models.SmallIntegerField(default=1)
    booking_date = models.DateField()
    booking_time = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_expired(self):
        if not self.booking_date or not self.booking_time:
            return False
        
        try:
            hour_int = int(self.booking_time)
            booking_time_obj = datetime.time(hour=hour_int, minute=0)
            booking_datetime = datetime.datetime.combine(self.booking_date, booking_time_obj)
            booking_datetime = timezone.make_aware(booking_datetime)
            return booking_datetime < timezone.now()

        except Exception as e:
            print(f"Error in is_expired: {e}")
            return False
    
    def __str__(self): 
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=False)
    inventory = models.BooleanField(default=False)
    category = models.ForeignKey(Categories,related_name="items", on_delete=models.CASCADE ,null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return f'{self.title} : {str(self.price)}'


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True) 
    email = models.EmailField()
    message_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

