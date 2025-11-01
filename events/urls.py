from django.urls import path

# import views for render the link:
from events.views import RegisterEventView,events_view, register_category ,editEventInfo ,deleteEvent ,category_view ,edit_category , delete_category
urlpatterns = [
    path('category/',category_view,name="category"),
    path('create-event/',RegisterEventView.as_view() , name="create-event"),
    path('events/',events_view,name="all-events"),
    path('create-category/',register_category,name="create-category"),
    path('edit-event/<int:id>/', editEventInfo , name="edit-event"),
    path('delete-event/<int:id>/',deleteEvent ,name="delete-event"),
    path('edit-category/<int:id>/',edit_category,name="edit-category"),
    path('delete-category/<int:id>/',delete_category,name="delete-category")
]
