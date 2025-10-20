from django.urls import path
from users.views import registerUserFormView , activate_user , login_user , logout_user

urlpatterns = [
    path('sign-in/',registerUserFormView, name='sign-in'),
    path('activate/<int:id>/<str:token>/',activate_user,name="activate-user"),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout')
]
