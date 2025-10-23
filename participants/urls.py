from django.urls import path

from participants.views import home ,Rsvp  ,event_details
urlpatterns = [
    path('home/',home,name="home"),
    path('details/<int:id>/',event_details,name="details"),
    path('rsvp/<int:id>/',Rsvp,name="rsvp"),
]
