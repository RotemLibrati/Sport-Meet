from django.db import models
from datetime import datetime

from django.db.models.deletion import SET_NULL

# Create your models here.


class Profile(models.Model):
    email = models.CharField(max_length=100, null=True,
                             blank=True, unique=True)
    address = models.CharField(max_length=100, default='')
    sex = models.CharField(max_length=10, choices=[
                           ('male', 'male'), ('female', 'female')])
    age = models.IntegerField(default=0)


class Team(models.Model):
    admin = models.ForeignKey(
        Profile, null=True, on_delete=SET_NULL, related_name='adminteam')
    members = models.ManyToManyField(Profile, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    sport = models.CharField(max_length=50, choices=[(
        'football', 'football'), ('basketball', 'basketball'), ('tennis', 'tennis')])


class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now)


class AppMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.now)


class GameField(models.Model):
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=200)


class Game(models.Model):
    team = models.ForeignKey(Team, models.CASCADE)
    event_time = models.DateTimeField()
    location = models.ForeignKey(
        GameField, null=True, on_delete=models.SET_NULL)
