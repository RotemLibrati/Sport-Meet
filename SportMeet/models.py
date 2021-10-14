from django.db import models

# Create your models here.
class Profile(models.Model):
    email = models.CharField(max_length=100, null=True, blank=True, unique=True)