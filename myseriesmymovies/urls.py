from django.urls import path
from core import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/<int:movie_id>/", views.add_to_library, name="add_to_library"),
]