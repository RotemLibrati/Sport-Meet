from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from SportMeet.models import Attendance, Game, Profile, Team, GameField, AppMessage, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    email = serializers.CharField()

    class Meta:
        model = Profile
        exclude = []


class GameFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameField
        exclude = []


class TeamSerializer(serializers.ModelSerializer):
    members = ProfileSerializer(required=False, many=True)
    admin = ProfileSerializer()

    class Meta:
        model = Team
        exclude = []


class GameSerializer(serializers.ModelSerializer):
    location = GameFieldSerializer()
    team = TeamSerializer()

    class Meta:
        model = Game
        exclude = []


class AppMessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()

    class Meta:
        model = AppMessage
        exclude = []


class AttendanceSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    game = GameSerializer()

    class Meta:
        model = Attendance
        exclude = []

class NotificationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Notification
        exclude = []