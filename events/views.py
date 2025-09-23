from django.shortcuts import render ,redirect
from django.contrib import messages
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


def admin_dashboard(request):
    events = Event.objects.all()

    events_cnt = events.count()
    print(events_cnt)
    context ={
        "events":events,
        'total_events': events_cnt,
    }
    return render(request,'dashboard.html',context)

def test(request):
    return render(request,'dashboard.html')