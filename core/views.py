import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Movie
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required
def dashboard(request):
    if request.method == "POST":
        query = request.POST.get("query")
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key":  settings.TMDB_API_KEY, "query": query},
        )
        print(response)
        movies = response.json().get("results", [])
        print(movies)
        return render(request, "dashboard.html", {"movies": movies})
    return render(request, "dashboard.html")

@login_required
def add_to_library(request, movie_id):
    if request.method == "POST":
        title = request.POST.get("title")
        rating = request.POST.get("rating")
        Movie.objects.create(user=request.user, movie_id=movie_id, title=title, rating=rating)
    return redirect("dashboard")
