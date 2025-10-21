from django.shortcuts import render ,redirect
from django.db.models import Q , Count
from django.contrib import messages
from django.utils import timezone 
from django.contrib.auth.decorators import login_required ,  user_passes_test
# import Register form from from.py:
from events.forms import CreateEventFrom , MakeCategoryFrom 

# import Model:
from events.models import Event ,Category

def is_admin(user):
    return user.groups.filter(name="Admin").exists()
def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()
def is_user(user):
    return user.groups.filter(name="User").exists()

# Create your views here.
@login_required
# @user_passes_test(is_organizer, login_url="no-access-page")
@user_passes_test(is_admin, login_url="no-access-page")
def register_event(request):
    if request.method == "POST":
        form = CreateEventFrom(request.POST , request.FILES)
        if form.is_valid():
            form.save()
        messages.success(request,"Event Register Successfully")
        return redirect('dashboard')
    else:
        form = CreateEventFrom()
    return render(request,'forms/event_form.html',{'form':form,"form_title":"Event Register"})

# register category:
@login_required
@user_passes_test(is_admin , login_url="no-access-page")
@user_passes_test(is_organizer, login_url="no-access-page")
def register_category(request):
    if request.method == "POST":
        form = MakeCategoryFrom(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request,"Category Register Successfully")
        return redirect('category')
    else:
        form = MakeCategoryFrom()
    return render(request,'form.html',{'form':form,"form_title":"Catefory Register"})



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
        return redirect('admin-dashboard')
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

