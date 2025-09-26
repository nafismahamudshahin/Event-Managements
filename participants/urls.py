from django.urls import path

from participants.views import home , register_participant , participant ,delete_participant, edit_participant ,event_details
urlpatterns = [
    path('home/',home,name="home"),
    path('details/<int:id>/',event_details,name="details"),
    path('create-participint/',register_participant , name="create-participint"),
    path('participant/',participant,name="participant"),
    path('delete-participant/<int:id>/',delete_participant,name="delete-participant"),
    path('edit-participant/<int:id>/',edit_participant,name="edit-participant")
]
