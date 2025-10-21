from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User , Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import login ,authenticate , logout
from users.forms import UserRegisterForm , UserLoginForm
from events.views import is_admin , is_organizer , is_user
from django.db.models import Q , Count
from django.utils import timezone 
from django.contrib.auth.decorators import login_required ,  user_passes_test
# import Register form from from.py:
from events.models import Participant ,Event
from participants.views import mail_send

# Create your views here.

def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_user(request.user):
        return redirect('user-dashboard')
    return redirect('no-access-page')


# user Dashboard:
def user_dashboard(request):
    return render(request,'user/user_dashboard.html')

# Organizer dashboard:
def organizer_dashboard(request):
    return render(request,"organizer/organizer_dashboard.html")

# This dashboard Render for Admin:
@login_required
@user_passes_test(is_admin , login_url="no-access-page")
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
    return render(request,'admin/admin_dashboard.html',context)


# user Register here:
def registerUserFormView(request):
   
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False
            user.save()
            return redirect("sign-up")
    else:
         form = UserRegisterForm()
    context = {
        "form": form,
    }
    return render(request,"user/sign_up.html",context)

# Activation User account and Wellcome message Send her mail:
def activate_user(request,id,token):
    print("word here")
    user = User.objects.get(id=id)
    try:
        if default_token_generator.check_token(user,token) and user.is_active == False:
            user.is_active = True
            user.save()
            subject = "congratulations 🎉"
            message = f"HI,{user.first_name} {user.last_name}\nSuccessfully verify Your account."
            recipient_email = [user.email]
            try:
                mail_send(subject,message,recipient_email)
            except Exception as e:
                print(f"Email not send to {user.email}: {str(e)}")
            return redirect('home')
        else:
            return HttpResponse("invalid id or token")
    except Exception as e:
        return HttpResponse(f"{str(e)}")

# login and log out:
def login_user(request):
    form= UserLoginForm()
    if request.method == "POST":
        form  = UserLoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            sub = "Sumone login your account"
            message = f"{user.first_name} are you sure now you are login your account"
            form_mail = 'nafismahamudshahin@gmail.com'
            redipient_mail = [user.email]
            send_mail(sub,message,form_mail,redipient_mail)
            print("problem")
            return redirect("home")
    context = {
        'form':form,
    }
    return render(request,'user/login.html',context)



def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")