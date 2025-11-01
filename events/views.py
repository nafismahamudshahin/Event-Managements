from django.shortcuts import render ,redirect
from django.utils.decorators import method_decorator
from django.db.models import Q , Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required ,  user_passes_test
from django.views.generic import CreateView , ListView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# import from my file:
from core.views import is_admin , is_organizer, is_user , is_admin_or_organizer , send_mail_to_user
from core.views import is_admin_or_organizer
from events.forms import CreateEventFrom , MakeCategoryFrom 
from events.models import Event ,Category

# this decorator store parmission for admin and organizer:
create_decorator = [login_required,user_passes_test(is_admin_or_organizer, login_url="no-permission")]

# Register Event view:
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
        
#view Events
class EventView(LoginRequiredMixin , ListView):
    model = Event
    template_name = "all_events.html"
    context_object_name = "events"

# Register Category:
@method_decorator(create_decorator , name="dispatch")
class RegisterCategoryView(CreateView):
    model = Category
    form_class = MakeCategoryFrom
    template_name = "form.html"
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Category Register"
        return context
    
    def get_success_url(self):
        messages.success(self.request,"Category Register Successfully")
        return super().get_success_url()

# view all Category
@method_decorator(create_decorator , name="dispatch")
class CategoryView(ListView):
    model = Category
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.prefetch_related("category").all() 
        return context

# Update Event:
@method_decorator(create_decorator , name="dispatch")
class EditEventView(UpdateView):
    model = Event
    form_class = CreateEventFrom
    template_name = "form.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("dashboard")

    def get_success_url(self):
        messages.success(self.request, "Event updated Successfully")
        return super().get_success_url()

# Delete Event:
@method_decorator(create_decorator , name="dispatch")
class DeleteEventView(DeleteView):
    model = Event
    template_name = "confirm.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("dashboard")

    def get_success_url(self):
        messages.success(self.request,"Event delete Successfully")
        return super().get_success_url()
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#Edit Category:
@method_decorator(create_decorator , name="dispatch")
class UpdateCategoryView(UpdateView):
    model = Category
    form_class = MakeCategoryFrom
    template_name = "form.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("category")

    def get_success_url(self):
        messages.success(self.request,"Category Updated Successfully")
        return super().get_success_url()


# delete category:
@method_decorator(create_decorator , name="dispatch")
class DeleteCategoryView(DeleteView):
    model = Category
    template_name = "confirm.html"
    pk_url_kwarg ="id"
    success_url = reverse_lazy("category")

    def get_success_url(self):
        messages.success(self.request,"Category Delete Successfully")
        return super().get_success_url()



