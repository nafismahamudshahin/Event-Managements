from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()
    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField()
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField()
    image = models.ImageField(upload_to="events_images", blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1 ,related_name="category")
    user = models.ManyToManyField(User, related_name="event")
    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField()
    email = models.EmailField()
    # event = models.ManyToManyField(Event,related_name="participant")
    def __str__(self):
        return self.name


