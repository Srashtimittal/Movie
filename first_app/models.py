from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters!"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"
        if postData['password'] != postData['pass_conf']:
            errors["pass_conf"] = "Password and Password Confirmation don't match!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # film_list = a list of movies a given user wants to see
    # watched = a list of movies a given user has seen


class FilmList(models.Model):
    title = models.CharField(max_length=255, default='')
    poster_path = models.CharField(max_length=255, default='')
    movie_id = models.IntegerField(default=0)
    users_added = models.ManyToManyField(User, related_name="film_list")
    users_watched = models.ManyToManyField(User, related_name="watched")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
