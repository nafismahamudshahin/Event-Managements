from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from users.forms import UserRegisterForm
# Create your views here.

# user Register here:
def registerUserFormView(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False
            user.save()
            return redirect("sign-in")
        
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
    pass

def logout_user(request):
    pass