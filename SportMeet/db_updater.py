from datetime import datetime
from numbers import Integral
from re import sub
from telnetlib import GA
from SportMeet.models import AppMessage, Attendance, City, GameField, Notification, Profile, Team, Game
from SportMeet import selectors
from django.contrib.auth.models import User
from django.utils import timezone
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
    def create_new_game(team: Team, location: GameField, event_time: datetime, limit_participants):
        game: Game = Game(team=team, location=location, event_time=event_time, limit_participants=limit_participants)
        game.save()
        return game
    
    def update_notification_field(game: Game):
        game.save()
        return game

    @staticmethod
    def update_game_details(game: Game):
        game.save()
        return game

    def delete_game_by_id(gameId):
        try:
            Game.objects.get(id=gameId).delete()
            return True
        except Game.DoesNotExist:
            return False


class GameFieldUpdater:
    @staticmethod
    def create_new_field_game(**kwargs):
        game_field: GameField = GameField(**kwargs)
        game_field.save()
        return game_field


class TeamUpdater:
    @staticmethod
    def create_new_team(admin=None, members=[], name=None, sport=None, anonymous=False, type='פומבית'):
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

    @staticmethod
    def update_details_team(team: Team):
        team.save()
        return team


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

class NotificationUpdater:
    @staticmethod
    def create_new_notification(profile: Profile, message: str):
        notification: Notification = Notification(
            profile=profile, message=message, is_seen=False, timestamp=timezone.now())
        notification.save()
        return notification
    
    @staticmethod
    def update_is_seen_field_to_true(notification: Notification):
        notification.save()
        return notification

class ImportCitiesUpdater:
    @staticmethod
    def add_cities_to_db(hebrew: str, english: str):
        city: City = City(hebrew_name=hebrew, english_name=english)
        city.save()
        return city





    