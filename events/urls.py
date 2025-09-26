from django.urls import path

# import views for render the link:
from events.views import register_event,register_category ,admin_dashboard ,editEventInfo ,deleteEvent ,category_management ,edit_category , delete_category
urlpatterns = [
    path('dashboard/',admin_dashboard,name="dashboard"),
    path('category/',category_management,name="category"),
    path('create-event/',register_event , name="create-event"),
    path('create-category/',register_category,name="create-category"),
    path('edit-event/<int:id>/', editEventInfo , name="edit-event"),
    path('delete-event/<int:id>/',deleteEvent ,name="delete-event"),
    path('edit-category/<int:id>/',edit_category,name="edit-category"),
    path('delete-category/<int:id>/',delete_category,name="delete-category")
]
