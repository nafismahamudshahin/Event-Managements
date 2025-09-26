from django.shortcuts import render ,redirect
from django.db.models import Q , Count
from django.contrib import messages
from django.utils import timezone 
# import Register form from from.py:
from events.forms import CreateEventFrom , MakeCategoryFrom 
from events.models import Participant

# import Model:
from events.models import Event ,Category
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
        return redirect('dashboard')
    else:
        form = MakeCategoryFrom()
    return render(request,'form.html',{'form':form})

# This dashboard Render for Admin:
def admin_dashboard(request):
    type = request.GET.get('type',"all")
    events = Event.objects.prefetch_related('category').all()
    now = timezone.localtime(timezone.now())
    counts_events = events.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=now.date()) | Q(date=now.date(), time__gt=now.time())),
        past = Count('id', filter = Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time()))
    )
    event_name = "All Event's"
    if type =="todayevents":
        events = events.filter(Q(date = now.date(), time__gt = now.time()))
        event_name = "Today's Events"
    elif type == "past":
        events = events.filter(Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time()))
        event_name = "Past Events"
    elif type == "upcoming":
        events = events.filter(Q(date__gt=now.date()) | Q(date=now.date(),time__gt = now.time()))
        event_name = "UpComing Events"

    context ={
        "events":events.order_by('date','time'),
        'count':counts_events,
        'event_name': event_name,
        "total_participants": Participant.objects.aggregate(total_count = Count('id'))
    }
    return render(request,'dashboard.html',context)

# Category:
def category_management(request):
    all_categorys = Category.objects.all()
    context={
        "categprys": all_categorys,
    }
    return render(request,"category.html",context)


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

# Delete Event:
def deleteEvent(request,id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('dashboard')

#Edit Category:
def edit_category(request,id):
    category = Category.objects.get(id=id)
    populate_form = MakeCategoryFrom(instance = category)
    if request == "POST":
        populate_form = MakeCategoryFrom(request.POST,instance = category)
        if populate_form.is_valid():
            populate_form.save()
            return redirect('category')
    return render(request,"form.html",{'form':populate_form})
# delete category:
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect("category")


def test(request):
    return render(request,'dashboard.html')
