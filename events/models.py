from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()

class Event(models.Model):
    name = models.CharField()
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)


class Participant(models.Model):
    name = models.CharField()
    email = models.EmailField()
    event = models.ManyToManyField(Event)


    