from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import login ,authenticate , logout
from users.forms import UserRegisterForm , UserLoginForm
# Create your views here.

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
            return redirect("sign-in")
    else:
         form = UserRegisterForm()
    context = {
        "form": form,
    }
    return render(request,"user/sign_in.html",context)

# Activation User account and Wellcome message Send her mail:
def activate_user(request,id,token):
    user = User.objects.get(id=id)
    try:
        if default_token_generator.check_token(user,token) and user.is_active == False:
            user.is_active = True
            user.save()
            subject = "congratulations 🎉"
            form_mail = "nafismahamudshahin@gmail.com"
            message = f"HI,{user.first_name} {user.last_name}\nSuccessfully verify Your account."
            recipient_email = [user.email]
            try:
                send_mail(subject,message,form_mail,recipient_email)
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