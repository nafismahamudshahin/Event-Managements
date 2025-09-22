from django.urls import path

# import views for render the link:
from events.views import test, register_event,register_participant,register_category ,admin_dashboard

urlpatterns = [
    path('test/',test),
    path('dashboard/',admin_dashboard,name="dashboard"),
    path('create-participint/',register_participant , name="create-participint"),
    path('create-event/',register_event , name="create-event"),
    path('create-category/',register_category,name="create-category")
]
