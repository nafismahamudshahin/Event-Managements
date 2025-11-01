from django.urls import path

# import views for render the link:
from events.views import RegisterEventView,EventView, RegisterCategoryView ,EditEventView ,DeleteEventView ,CategoryView ,UpdateCategoryView , DeleteCategoryView
urlpatterns = [
    path('category/',CategoryView.as_view(),name="category"),
    path('create-event/',RegisterEventView.as_view() , name="create-event"),
    path('events/',EventView.as_view(),name="all-events"),
    path('create-category/',RegisterCategoryView.as_view(),name="create-category"),
    path('edit-event/<int:id>/', EditEventView.as_view(), name="edit-event"),
    path('delete-event/<int:id>/',DeleteEventView.as_view(),name="delete-event"),
    path('edit-category/<int:id>/',UpdateCategoryView.as_view(),name="edit-category"),
    path('delete-category/<int:id>/',DeleteCategoryView.as_view(),name="delete-category")
]
