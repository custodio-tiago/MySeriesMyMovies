from django.urls import path
from core import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/<int:movie_id>/", views.add_to_library, name="add_to_library"),
    path("library/", views.user_library, name="user_library"),
    path("update/<int:movie_id>/", views.update_rating, name="update_rating"),
    path("delete/<int:movie_id>/", views.delete_movie, name="delete_movie"),
]
