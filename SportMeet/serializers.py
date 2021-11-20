from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from SportMeet import models
from SportMeet.models import Game, Profile, Team, GameField, AppMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Profile
        exclude = []


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        exclude = []


class TeamSerializer(serializers.ModelSerializer):
    members = ProfileSerializer(required=False, many=True)
    admin = ProfileSerializer()

    class Meta:
        model = Team
        exclude = []


class GameFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameField
        exclude = []


class AppMessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    
    class Meta:
        model = AppMessage
        exclude = []
