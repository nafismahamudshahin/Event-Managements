from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    path('',include('participants.urls')),
    path('',include('dashboard.urls')),
    path('',include('categories.urls')),
]
