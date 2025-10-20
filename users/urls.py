from django.urls import path
from users.views import *

urlpatterns = [
    path('sign-in/',registerUserFormView, name='sign-in'),
    path('activate/<int:id>/<str:token>/',activate_user,name="activate-user")
]
