from datetime import datetime
from re import sub
from SportMeet.models import AppMessage, Attendance, GameField, Profile, Team, Game
from SportMeet import selectors
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os


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
        # if 'email' in data:
        #     data['email'] = Profile.encode_and_encrypt_email(data['email'])
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
    def create_new_field_game(**kwargs):
        game_field: GameField = GameField(**kwargs)
        game_field.save()
        return game_field


class TeamUpdater:
    @staticmethod
    def create_new_team(admin=None, members=[], name=None, sport=None, anonymous=False, type=None):
        team: Team = Team(admin=admin, name=name,
                          sport=sport, anonymous=anonymous, type=type)
        team.save()
        for m in members:
            team.members.add(m)
        return team
    
    @staticmethod
    def delete_team_by_id(id):
        Team.objects.filter(id=id).delete()
        return

class AppMessageUpdater:
    @staticmethod
    def change_seen_for_messgae(message: AppMessage):
        message.save()
        return message

    @staticmethod
    def post_message(sender: Profile, subject: str, body: str, timestamp: datetime, team: Team):
        message: AppMessage = AppMessage(
            sender=sender, subject=subject, body=body, timestamp=timestamp, team=team)
        message.save()
        return message
    
    @staticmethod
    def delete_message_by_id(messageId):
        try:
            AppMessage.objects.get(id=messageId).delete()
            return True
        except AppMessage.DoesNotExist:
            return False


class AttendanceUpdater:
    @staticmethod
    def create_attendance(profile: Profile, game: Game, status):
        attendace: Attendance = Attendance(
            profile=profile, game=game, status=status)
        attendace.save()
        return attendace

    def change_attendance(attendance: Attendance):
        attendance.save()
        return attendance
