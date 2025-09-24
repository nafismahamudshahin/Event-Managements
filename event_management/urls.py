from django.contrib import admin
from django.urls import path ,include
from debug_toolbar.toolbar import debug_toolbar_urls
from participants.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('',include('events.urls')),
    path('',include('participants.urls')),
    path('',include('dashboard.urls')),
    path('',include('categories.urls')),
]+debug_toolbar_urls()

