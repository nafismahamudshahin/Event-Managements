from django.urls import path
from users.views import registerUserFormView,EditProfileView ,CustomChangePasswordView, CustomPasswordResetView,CustomPasswordResetConfirmView, activate_user,profile ,delete_user, login_user , logout_user , dashboard ,admin_dashboard, user_dashboard , organizer_dashboard, change_role , create_group , delete_group

urlpatterns = [
    path('sign-up/',registerUserFormView, name='sign-up'),
    path('activate/<int:id>/<str:token>/',activate_user,name="activate-user"),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('dashboard/',dashboard,name="dashboard"),
    path('admin-dashboard/',admin_dashboard,name="admin-dashboard"),
    path('user-dashboard/',user_dashboard,name="user-dashboard"),
    path('organizer-dashboard/',organizer_dashboard,name="organizer-dashboard"),
    path('create-group/',create_group,name="create-group"),
    path('delete-group/<int:id>/',delete_group,name="delete-group"),
    path('delete-user/<int:id>/',delete_user,name="delete-user"),
    path('change-role/<int:id>/',change_role,name="change-role"),
    path('profile',profile,name="profile"),
    path('edit-profile/',EditProfileView.as_view(),name="edit-profile"),
    path('change-password/',CustomChangePasswordView.as_view(),name="change-password"),
    path('reset-password/',CustomPasswordResetView.as_view(),name="reset-password"),
    path('password_reset_confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name="password_reset_confirm")
]
