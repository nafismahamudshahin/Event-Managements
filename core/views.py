from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.

def send_mail_to_user(sub, message , to_mail):
    from_mail = 'nafismahamudshahin@gmail.com'
    try:
        send_mail(sub,message,from_mail,to_mail)
    except Exception as e:
        print(f"Messages not send for : {str(e)}")

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_organizer(user):
    return user.groups.filter(name="organizer").exists()

def is_user(user):
    return user.groups.filter(name="User").exists()

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

def no_access_pages(request):
    return render(request,'no_access_page.html')