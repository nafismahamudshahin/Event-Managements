from django.urls import path
from core.views import no_access_pages
urlpatterns = [
    path('no-access-page/',no_access_pages, name="no-access-page")
]
