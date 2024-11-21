import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Movie
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # URL base para imagens

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
            params={"api_key": settings.TMDB_API_KEY, "query": query},
        )
        movies = response.json().get("results", [])
        # Passar a lista de filmes para o template
        return render(request, "dashboard.html", {"movies": movies})
    return render(request, "dashboard.html")

@login_required
def add_to_library(request, movie_id):
    if request.method == "POST":
        # Fazer uma requisição para obter os detalhes completos do filme
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": settings.TMDB_API_KEY},
        )
        movie_data = response.json()
        title = movie_data.get("title")
        rating = request.POST.get("rating")
        # Obter a URL da imagem (pode ser `poster_path`, `backdrop_path`, ou outro campo relevante)
        image_url = TMDB_IMAGE_BASE_URL + movie_data.get("poster_path", "")

        # Criar o filme na biblioteca do usuário
        Movie.objects.create(user=request.user, movie_id=movie_id, title=title, rating=rating, image_url=image_url)

    return redirect("user_library")

@login_required
def user_library(request):
    # Recupera os filmes da biblioteca do usuário
    movies = Movie.objects.filter(user=request.user)
    return render(request, "userlibrary.html", {"movies": movies})

@login_required
def update_rating(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id, user=request.user)
        movie.rating = request.POST.get("rating")
        movie.save()
    return redirect("user_library")

@login_required
def delete_movie(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id, user=request.user)
        movie.delete()
    return redirect("user_library")

# Função de logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')  # Redireciona para a página de login
