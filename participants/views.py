from django.shortcuts import render
from events.models import Event,Participant,Category
# Create your views here.

def home(request):
    return render(request,'home.html')