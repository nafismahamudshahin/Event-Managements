from django.shortcuts import render , redirect , HttpResponse
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone 
from datetime import datetime
from django.contrib import messages
from events.models import Event,Participant , Category
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required , user_passes_test
from core.views import is_admin , is_organizer, is_user , is_admin_or_organizer , send_mail_to_user
# chenged here


# view Participant:
@user_passes_test(is_admin, login_url="no-access-page")
def participant(request):
    allUser = User.objects.all()
    context ={
        "users": allUser,
    }
    return render(request,"user_list.html",context)

def home(request):
    type = request.GET.get('type',"all")
    query = request.GET.get("search_query")
    todaytime = timezone.localdate(timezone.now())

    events = Event.objects.select_related('category').all()
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

@login_required
def Rsvp(request , id):
    url_r = request.GET.get('next','home')
    event = Event.objects.get(id=id)
    if request.user not in event.participant.all():
        event.participant.add(request.user)
        messages.success(request,"Successfully Register")
        sub = "Successfully Register Event"
        user = request.user
        message = f"Hello , {user.first_name} {user.last_name}\nYou Registation Successfully Completed in {event.name}"
        to_mail = [user.email]
        send_mail_to_user(sub,message,to_mail)
    else:
        messages.success(request,"This Event you already book")
    return redirect(url_r)

