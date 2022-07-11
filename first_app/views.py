from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from tmdbv3api import TMDb, Collection, Movie, Search

tmdb = TMDb()
tmdb.api_key = ''
tmdb.language = "en"

# ----------------- Login & Registration ----------------


def index(request):
    return render(request, "index.html")

# ----------------- Login Route -------------------------


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/movies')
        else:
            messages.error(request, "Oops, those credentials are invalid!")
            return redirect('/')
    else:
        messages.error(request, "Oops, those credentials are invalid!")

        return redirect('/')


# ----------------- Create New User ---------------------

def sign_up(request):
    return render(request, "sign_up.html")


# ----------------- Create New User Route ---------------------


def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')

    hash = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print(hash)

    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hash
    )
    request.session['userid'] = new_user.id

    return redirect('/movies')


# --------------------- Profile Route -----------------------


def profile(request):
    this_user = User.objects.get(id=request.session['userid'])

    context = {
        "this_user": this_user
    }

    return render(request, "profile.html", context)


# --------------------- Update Route -----------------------

def update(request, user_id):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/profile')
    else:
        user = User.objects.get(id=request.session['userid'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()

    return redirect('/profile')


# ----------------------- Home Page -------------------------

def movies(request):
    movie = Movie()
    latest = movie.latest()
    now_playing = movie.now_playing()
    top_rated = movie.top_rated()
    upcoming = movie.upcoming()
    popular = movie.popular()
    posterUrl = 'https://image.tmdb.org/t/p/original/'
    context = {
        "this_user": User.objects.get(id=request.session['userid']),
        "popular": popular,
        "latest": latest,
        "now_playing": now_playing,
        "top_rated": top_rated,
        "upcoming": upcoming,
        "poster": posterUrl,
    }

    return render(request, "movies.html", context)

# ----------------------- Single Movie Page -------------------------


def movie(request, movie_id):
    movie = Movie()
    video = movie.videos(movie_id)
    this_movie = movie.details(movie_id)
    posterUrl = 'https://image.tmdb.org/t/p/original/'

    context = {
        "movie": movie,
        "poster": posterUrl,
        "this_movie": this_movie,
        "video": video
    }

    return render(request, "movie.html", context)


# ---------------------- My List ---------------------------


def my_list(request):
    movie = Movie()
    posterUrl = 'https://image.tmdb.org/t/p/original'
    context = {
        "this_user": User.objects.get(id=request.session['userid']),
        "movie": movie,
        "poster": posterUrl,
    }
    return render(request, "my_list.html", context)


# ---------------------- Watched Page ---------------------------


def watched(request):
    this_user = User.objects.get(id=request.session['userid'])
    posterUrl = 'https://image.tmdb.org/t/p/original'
    context = {
        "this_user": this_user,
        "poster": posterUrl,
    }

    return render(request, "watched.html", context)


# --------------------- Sign Out Route -----------------------

def signout(request):
    request.session.clear()
    messages.error(request, "Successfully logged out")

    return redirect('/')


# --------------------- Add To Filmlist Route -----------------------
def add_to_list(request, movie_id):
    user = User.objects.get(id=request.session['userid'])

    movie = FilmList.objects.create(
        movie_id=movie_id,
        title=request.POST['movie_title'],
        poster_path=request.POST['movie_poster_path']
    )
    movie.save()
    movie.users_added.add(request.session['userid'])
    return redirect('/my_list')


# --------------------- Add To Watched Route -----------------------
def add_to_watched(request, movie_id):
    user = User.objects.get(id=request.session['userid'])
    movie = movie_id
    user.watched.add(movie)
    user.film_list.remove(movie)
    return redirect('/my_list')

# --------------------- Remove From Filmlist Route -----------------------


def remove_from_list(request, movie_id):
    user = User.objects.get(id=request.session['userid'])
    movie = movie_id
    user.film_list.remove(movie)
    return redirect('/my_list')

# --------------------- Remove From Watched Route -----------------------


def remove_from_watched(request, movie_id):
    user = User.objects.get(id=request.session['userid'])
    movie = movie_id
    user.watched.remove(movie)
    return redirect('/watched')


# --------------------- Search -----------------------

def search(request):
    return render(request, "search.html")
