from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User , Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login , logout
from users.forms import UserRegisterForm , UserLoginForm
from core.views import is_admin , is_organizer, is_user , is_admin_or_organizer , send_mail_to_user
from django.db.models import Q , Count
from django.utils import timezone 
from django.contrib import messages
from django.contrib.auth.decorators import login_required ,  user_passes_test
from users.forms import ChangeRoleForm , GroupForm
from django.shortcuts import get_object_or_404

# import Register form from from.py:
from events.models import  Event

# Create your views here.
@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_user(request.user):
        return redirect('user-dashboard')
    return redirect('no-access-page')


# user Dashboard:
@user_passes_test(is_user,login_url="no-access-page")
def user_dashboard(request):
    user = request.user
    context = {
        "user":user,
    }
    return render(request,'user/user_dashboard.html' , context)

# Organizer dashboard:
@user_passes_test(is_organizer,login_url='no-access-page')
def organizer_dashboard(request):
    type = request.GET.get('type',"all")
    events = Event.objects.prefetch_related('category').prefetch_related("participant").all()
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

    context = {
        "events":events.order_by('date','time'),
        'count':counts_events,
        'event_name': event_name,
        "total_participants": User.objects.aggregate(total_count = Count('id'))
    }
    return render(request,"organizer/organizer_dashboard.html",context)

# This dashboard Render for Admin:
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
    groups = Group.objects.all()
    context ={}
    if type == "participants":
        context ={
            'participants': User.objects.all(),
            'count':counts_events,
            'event_name': "All Participants",
            'type':'participants',
            'group_cnt': groups.count(),
            "total_participants": User.objects.aggregate(total_count = Count('id'))
        }
    elif type == "groups":
        context ={
            "groups": groups,
            'count':counts_events,
            'event_name': "All Group's",
            'type':"groups",
            'group_cnt': groups.count(),
            "total_participants": User.objects.aggregate(total_count = Count('id'))
        }
    else:
        context ={
            "events":events.order_by('date','time'),
            'count':counts_events,
            'event_name': event_name,
            'type':"other",
            'group_cnt': groups.count(),
            "total_participants": User.objects.aggregate(total_count = Count('id'))
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
            messages.success(request,"Please Check your Email and Verify.")
            return redirect("login")
        else:
            messages.error(request,"Invalid Information")
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
                send_mail_to_user(subject,message,recipient_email)
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
            sub = "Someone login your account"
            message = f"{user.first_name} are you sure now you are login your account"
            recipient_mail = [user.email]
            send_mail_to_user(sub,message,recipient_mail)
            return redirect("home")
        else:
            messages.error(request,"Invalid Login information")
    context = {
        'form':form,
    }
    return render(request,'user/login.html',context)



def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    
# chenge user access role:
@user_passes_test(is_admin,login_url="no-access-page")
def change_role(request,id):
    user = get_object_or_404(User,id=id)
    form = ChangeRoleForm()
    if request.method == "POST":
        form = ChangeRoleForm(request.POST)
        if form.is_valid():
            choice_role = form.cleaned_data.get('choice_role')
            user.groups.clear()
            group = get_object_or_404(Group, name=choice_role)
            user.groups.add(group)
            user.save()
            messages.success(request,"Successfully Chenge user Role.")
            return redirect("dashboard")
        else:
            messages.error(request,"Not chenge role.")
    return render(request,'admin/role_change.html',{'form':form})

# create use access role or Group
@user_passes_test(is_admin,login_url="no-access-page")
def create_group(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            permissions = form.cleaned_data.get('permissions')
            if Group.objects.filter(name=name).exists() == False:
                group = Group.objects.create(name=name)
                group.permissions.set(permissions)
                group.save()
                messages.success(request,"Successfully Created a new Group")
                return redirect("dashboard")
            else:
                messages.error(request,"This Group Already Existsp")
                print("This Group Already Exists")
    return render(request,"admin/create_group.html",{'form':form})

# delete group:
def delete_group(request,id):
    group = Group.objects.get(id=id)
    group_name = group.name
    if request.method == "POST":
        group.delete()
        messages.success(request,f"{group_name} delete Successfully.")
    else:
        messages.error(request,"group not delete.")
    return redirect("dashboard")