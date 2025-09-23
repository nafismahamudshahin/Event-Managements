from django.shortcuts import render ,redirect
from django.db.models import Q , Count
from django.contrib import messages
from django.utils import timezone 
# import Register form from from.py:
from events.forms import CreateEventFrom , MakeCategoryFrom , RegisterParticipantFrom

# import Model:
from events.models import Event , Participant ,Category
# Create your views here.
def register_event(request):
    if request.method == "POST":
        form = CreateEventFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Event Register Successfully")
        return redirect('dashboard')
    else:
        form = CreateEventFrom()
    return render(request,'form.html',{'form':form})

# register category:
def register_category(request):
    if request.method == "POST":
        form = MakeCategoryFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Category Register Successfully")
        return redirect('create-category')
    else:
        form = MakeCategoryFrom()
    return render(request,'form.html',{'form':form})

# Register Participant:
def register_participant(request):
    if request.method == "POST":
        form = RegisterParticipantFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Participant Register Successfully")
        return redirect('create-participint')
    else:
        form = RegisterParticipantFrom()
    return render(request,'form.html',{'form':form})

# This dashboard Render for Admin:
def admin_dashboard(request):
    type = request.GET.get('type',"all")
    events = Event.objects.all()
    now = timezone.localtime(timezone.now())
    counts_events = events.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=now.date()) | Q(date=now.date(), time__gt=now.time())),
        past = Count('id', filter = Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time()))
    )

    if type =="todayevents":
        events = events.filter(Q(date = now.date(), time__gt = now.time()))
    elif type == "past":
        events = events.filter(Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time()))
    elif type == "upcoming":
        events = events.filter(Q(date__gt=now.date()) | Q(date=now.date(),time__gt = now.time()))

    context ={
        "events":events,
        'count':counts_events
    }
    return render(request,'dashboard.html',context)

# Edit Event information:
def editEventInfo(request,id):
    event = Event.objects.get(id=id)
    form = CreateEventFrom(instance = event)
    if request.method == "POST":
        form = CreateEventFrom(request.POST,instance = event)
        if form.is_valid():
            form.save()
        messages.success(request,"Event updated Successfully")
        return redirect('dashboard')
    return render(request,'form.html',{'form':form})



def test(request):
    return render(request,'dashboard.html')