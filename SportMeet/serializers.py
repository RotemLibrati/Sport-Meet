from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from SportMeet import models
from SportMeet.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Profile
        exclude = []
