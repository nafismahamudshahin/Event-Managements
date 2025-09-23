from django.urls import path

from participants.views import home

urlpatterns = [
    path('home/',home,name="home")
]
