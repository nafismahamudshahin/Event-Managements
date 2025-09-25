from django.shortcuts import render , redirect
from django.utils import timezone 
from datetime import datetime
from django.contrib import messages
from events.models import Event,Participant
from participants.forms import RegisterParticipantFrom

# Create your views here.
# Register Participant:
def register_participant(request):
    if request.method == "POST":
        form = RegisterParticipantFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Participant Register Successfully")
        return redirect('participant')
    else:
        form = RegisterParticipantFrom()
    return render(request,'form.html',{'form':form})

# view Participant:
def participant(request):
    allParticipants = Participant.objects.all()
    context ={
        "participants": allParticipants,
    }
    return render(request,"participants.html",context)


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

# delete
def delete_participant(request,id):
    participant = Participant.objects.get(id=id)
    participant.delete()
    return redirect("participant")
