from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup', views.sign_up),
    path('register', views.register),
    path('signout', views.signout),
    path('profile', views.profile),
    path('update/<int:user_id>', views.update),
    path('movie/<int:movie_id>', views.movie),
    path('movies', views.movies),
    path('add_to_watched/<int:movie_id>', views.add_to_watched),
    path('add_to_list/<int:movie_id>', views.add_to_list),
    path('remove/<int:movie_id>', views.remove_from_list),
    path('remove_from_watched/<int:movie_id>', views.remove_from_watched),
    path('my_list', views.my_list),
    path('watched', views.watched),
    path('search', views.search),
]

urlpatterns += staticfiles_urlpatterns()
