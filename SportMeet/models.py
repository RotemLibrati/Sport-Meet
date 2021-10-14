from django.db import models

# Create your models here.
class Profile(models.Model):
    SEX = (('male', 'male'), ('female', 'female'))
    email = models.CharField(max_length=100, null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, default='')
    sex = models.CharField(max_length=10, choices=SEX)
    age = models.IntegerField(default=0)


class Team(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    sport = models.CharField(max_length=50, choices=[('football', 'football'), ('basketball', 'basketball'), ('tennis', 'tennis')])
    
class TeamPrivileges(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.OneToOneField(Profile, on_delete=models.CASCADE)
    can_invite_new_members = models.BooleanField(default=False, blank=True)