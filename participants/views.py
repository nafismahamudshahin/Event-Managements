from django.shortcuts import render , redirect
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone 
from datetime import datetime
from django.contrib import messages
from events.models import Event,Participant , Category
from participants.forms import RegisterParticipantFrom

# Create your views here.
# Register Participant:
def register_participant(request):
    if request.method == "POST":
        form = RegisterParticipantFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Participant Register Successfully")
        return redirect('home')
    else:
        form = RegisterParticipantFrom()
    return render(request,'form.html',{'form':form,"form_title":"Participant Register"})

def register_participant_for_admin(request):
    if request.method == "POST":
        form = RegisterParticipantFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Participant Register Successfully")
        return redirect('participant')
    else:
        form = RegisterParticipantFrom()
    return render(request,'form.html',{'form':form,"form_title":"Participant Register"})

# view Participant:
def participant(request):
    allParticipants = Participant.objects.all()
    context ={
        "participants": allParticipants,
    }
    return render(request,"participants.html",context)


def home(request):
    type = request.GET.get('type',"all")
    query = request.GET.get("search_query")
    todaytime = timezone.localdate(timezone.now())

    events = Event.objects.select_related('category').prefetch_related('participant').all()
    filter_events = None
    start = None
    end = None
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            filter_events = events.filter(date__range=(start, end))
    if type != "all":
        events = events.filter(category__name=type)

    search_results =[]
    if query:
        query = query.lower()
        search_results = events.annotate(
            cat_lower=Lower('category__name')
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(cat_lower__contains=query)
        )

    context = {
        "events": events ,
        'today_events': events.filter(date = todaytime),
        'filter_events': filter_events,
        'catetorys': Category.objects.all(),
        'search_results':search_results,
        'time': todaytime,
        'start_time': start,
        'end_time': end,
        'query': query,
    }
    return render(request,'home.html',context)

# show event details:
def event_details(request,id):
    event = Event.objects.select_related('category').get(id=id)
    return render(request,"details.html",{'event':event})
# edit:

def edit_participant(request,id):
    participant = Participant.objects.get(id=id)
    form = RegisterParticipantFrom(instance = participant)
    if request.method == "POST":
        form = RegisterParticipantFrom(request.POST,instance = participant)
        if form.is_valid():
            form.save()
        return redirect('participant')
    return render(request,'form.html',{'form':form})

# delete
def delete_participant(request,id):
    participant = Participant.objects.get(id=id)
    participant.delete()
    return redirect("participant")

