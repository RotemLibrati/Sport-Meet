from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.db.models.fields import BooleanField, CharField


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True,
                             blank=True, unique=True)
    city = models.CharField(max_length=100, default='')
    sex = models.CharField(max_length=10, choices=[
                           ('זכר', 'זכר'), ('נקבה', 'נקבה')])
    age = models.IntegerField(default=0)


class Team(models.Model):
    admin = models.ForeignKey(
         Profile, null=True, on_delete=models.SET_NULL, related_name='adminteam', blank=True)
    members = models.ManyToManyField(Profile, blank=True, related_name='team')
    name = models.CharField(max_length=50, null=True, blank=True)
    sport = models.CharField(max_length=50, choices=[(
        'כדורגל', 'כדורגל'), ('כדורסל', 'כדורסל'), ('טניס', 'טניס')])
    anonymous = models.BooleanField(default=False)
    #type = models.CharField(max_length=20, choices=[("פומבית", "פומבית"), ("פרטית", "פרטית")])


class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now)


class AppMessage(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.now)
    seen = models.BooleanField(default=False)


class GameField(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    address_number = CharField(max_length=5)
    is_for_football = BooleanField(default=False)
    is_for_basketball = BooleanField(default=False)
    is_for_tennis = BooleanField(default=False)
    telephone = models.CharField(max_length=20)
    availability = models.CharField(max_length=50)


class Game(models.Model):
    team = models.ForeignKey(Team, models.CASCADE, related_name='game')
    event_time = models.DateTimeField()
    location = models.ForeignKey(
        GameField, null=True, on_delete=models.SET_NULL)

class Attendance(models.Model):
    status = models.CharField(max_length=10, null=True, blank=True, choices=[
                           ('מגיע', 'מגיע'), ('לא מגיע', 'לא מגיע'), ('אולי מגיע', 'אולי מגיע')])
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)