from django.shortcuts import render , redirect
from django.utils import timezone 
from datetime import datetime
from events.models import Event,Participant,Category
# Create your views here.

def home(request):
    todaytime = timezone.localdate(timezone.now())
    events = Event.objects.all()
    filter_events = None
    if request.method == "POST":
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            filter_events = events.filter(date__range=(start, end))
            
    context = {
        "events": events ,
        'today_events': events.filter(date = todaytime),
        'filter_events': filter_events,
        'time': todaytime,
    }
    return render(request,'home.html',context)