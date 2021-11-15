from datetime import time
from SportMeet.models import AppMessage, GameField, Profile, Team, Game
from django.contrib.auth.models import User
#from datetime import datetime
from django.utils import timezone


class ProfileSelector:

    @staticmethod
    def all_objects():
        return Profile.objects.all()

    @staticmethod
    def one_obj_by_email(email):
        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist as e:
            raise e
        return profile

    @staticmethod
    def get_details_profile(username):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        return profile

    


class UserSelector:
    @staticmethod
    def all_users():
        return User.objects.all()


class GameSelector:

    @staticmethod
    def three_obj_in_the_future_by_username(username: str):
        user = User.objects.get(username=username)
        teams = user.profile.team.all()
        _now = timezone.now()
        games = Game.objects.filter(
            team__in=teams, event_time__gte=_now).order_by('event_time')[0:3]
        return games
    
    @staticmethod
    def many_obj_in_the_future_by_username(username: str):
        user = User.objects.get(username=username)
        teams = user.profile.team.all()
        _now = timezone.now()
        games = Game.objects.filter(
            team__in=teams, event_time__gte=_now).order_by('event_time')
        return games

    @staticmethod
    def one_obj_by_id(id: str):
        return Game.objects.get(id=id)



class TeamSelector:

    @staticmethod
    def three_obj_by_username(username):
        user: User = User.objects.get(username=username)
        teams = user.profile.team.filter(anonymous=False)[0:3]
        return teams

    @staticmethod
    def all_obj_by_username(username):
        user: User = User.objects.get(username=username)
        teams = user.profile.team.filter(anonymous=False)
        return teams
    
    @staticmethod
    def get_obj_by_id(id):
        try:
            team = Team.objects.get(pk=id)
        except Team.DoesNotExist as e:
            raise e
        return team

class GameFieldSelector:

    @staticmethod
    def all_game_field():
        game_field: GameField = GameField.objects.all()
        return game_field

    @staticmethod
    def get_game_field_by_id(id):
        try:
            game_field = GameField.objects.get(pk=id)
        except GameField.DoesNotExist as e:
            raise e
        return game_field

class AppMessageSelector:

    @staticmethod
    def get_message_by_team_id(id):
        try:
            message = AppMessage.objects.filter(team__id=id)
        except AppMessage.DoesNotExist as e:
            raise e
        return message