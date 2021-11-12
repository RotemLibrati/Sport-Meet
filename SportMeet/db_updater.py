from datetime import datetime
from SportMeet.models import GameField, Profile, Team, Game
from SportMeet import selectors
from django.contrib.auth.models import User


class ProfileUpdater:
    @staticmethod
    def update_user_by_email(email, **kwargs):
        try:
            profile = selectors.ProfileSelector.one_obj_by_email(email)
        except Profile.DoesNotExist as e:
            raise e
        for key, val in kwargs.items():
            setattr(profile, key, val)
        profile.save()

    @staticmethod
    def create_new_profile_for_user(user: User, data: dict):
        profile: Profile = Profile(user=user, **data)
        profile.save()
        return profile

    @staticmethod
    def update_deailts_profile(profile: Profile):
        profile.save()
        return profile


class UserUpdater:
    @staticmethod
    def create_new_user(data: dict):
        _password = data['password']
        del data['password']
        user = User(**data)
        user.set_password(_password)
        user.save()
        return user


class GameUpdater:
    @staticmethod
    def create_new_game(team: Team, location: GameField, event_time: datetime):
        game: Game = Game(team=team, location=location, event_time=event_time)
        game.save()
        return game


class GameFieldUpdater:
    @staticmethod
    def create_new_field_game(city: str, address: str):
        game_field: GameField = GameField(city=city, address=address)
        game_field.save()
        return game_field


class TeamUpdater:
    @staticmethod
    def create_new_team(admin=None, members=[], name=None, sport=None):
        team: Team = Team(admin=admin, name=name, sport=sport)
        team.save()
        for m in members:
            team.members.add(m)
        return team
