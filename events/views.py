from django.shortcuts import render ,redirect
from django.utils.decorators import method_decorator
from django.db.models import Q , Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required ,  user_passes_test
from core.views import is_admin_or_organizer

# import Register form from from.py:

from events.forms import CreateEventFrom , MakeCategoryFrom 
from core.views import is_admin , is_organizer, is_user , is_admin_or_organizer , send_mail_to_user
# import Model:
from events.models import Event ,Category
from django.views.generic import CreateView

create_decorator = [login_required,user_passes_test(is_admin_or_organizer, login_url="no-permission")]

@method_decorator(create_decorator , name="dispatch")
class RegisterEventView(CreateView):
    model = Event
    form_class = CreateEventFrom
    template_name = "forms/event_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Event Register"
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Event Register Successfully")
        return redirect("dashboard")
        
    

# view events:
@login_required
def events_view(request):
    events = Event.objects.all()
    context ={
        'events': events
    }
    return render(request,"all_events.html", context)

# register category:
@user_passes_test(is_admin_or_organizer, login_url="no-access-page")
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
@user_passes_test(is_admin_or_organizer, login_url="no-access-page")
def category_view(request):
    all_categorys = Category.objects.prefetch_related("category").all()
    context={
        "categprys": all_categorys,
    }
    return render(request,"category.html",context)


# Edit Event information:
@user_passes_test(is_admin_or_organizer, login_url="no-access-page")
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
@user_passes_test(is_admin_or_organizer, login_url="no-access-page")
def deleteEvent(request,id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request,"Event delete Successfully")
    return redirect('dashboard')

#Edit Category:
@user_passes_test(is_admin_or_organizer, login_url="no-access-page") #problem here not updated error
def edit_category(request,id):
    category = Category.objects.get(id=id)
    populate_form = MakeCategoryFrom(instance = category)
    if request.method == "POST":
        populate_form = MakeCategoryFrom(request.POST, instance = category)
        if populate_form.is_valid():
            populate_form.save()
            messages.success(request,"Category Updated Successfully")
            return redirect('category')
        else:
            messages.error(request,"Not Updated")
            return redirect("category")
    return render(request,"form.html",{'form':populate_form})

# delete category:
@user_passes_test(is_admin_or_organizer, login_url="no-access-page")
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request,"Category Delete Successfully")
    return redirect("category")

