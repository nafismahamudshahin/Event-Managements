from django.urls import path

from participants.views import home , register_participant , participant ,delete_participant
urlpatterns = [
    path('home/',home,name="home"),
    path('create-participint/',register_participant , name="create-participint"),
    path('participant/',participant,name="participant"),
    path('delete-participant/<int:id>/',delete_participant,name="delete-participant")
]
