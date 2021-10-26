from SportMeet.models import Profile, Team, Game
from django.contrib.auth.models import User
from datetime import datetime


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


class UserSelector:
    @staticmethod
    def all_users():
        return User.objects.all()


class GameSelector:

    @staticmethod
    def three_obj_in_the_future_by_username(username: str):
        user = User.objects.get(username=username)
        teams = user.profile.team.all()
        _now = datetime.now()
        games = Game.objects.filter(
            team__in=teams, event_time__gte=_now).order_by('event_time')[0:4]
        return games


class TeamSelector:

    @staticmethod
    def three_obj_by_username(username):
        user: User = User.objects.get(username=username)
        teams = user.profile.team.all()[0:4]
        return teams
