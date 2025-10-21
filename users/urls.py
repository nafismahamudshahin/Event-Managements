from django.urls import path
from users.views import registerUserFormView , activate_user , login_user , logout_user , dashboard ,admin_dashboard, user_dashboard , organizer_dashboard

urlpatterns = [
    path('sign-up/',registerUserFormView, name='sign-up'),
    path('activate/<int:id>/<str:token>/',activate_user,name="activate-user"),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('dashboard/',dashboard,name="dashboard"),
    path('admin-dashboard/',admin_dashboard,name="admin-dashboard"),
    path('user-dashboard/',user_dashboard,name="user-dashboard"),
    path('organizer-dashboard/',organizer_dashboard,name="organizer-dashboard")
]
