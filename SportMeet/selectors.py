from datetime import time
from SportMeet.models import AppMessage, Attendance, GameField, Notification, Profile, Team, Game
from django.contrib.auth.models import User
from SportMeet import db_updater
from datetime import datetime, timedelta
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
    def all_upcoming_games(username: str):
        user = User.objects.get(username=username)
        teams = user.profile.team.all()
        _now = timezone.now()
        games = Game.objects.filter(
            team__in=teams, event_time__gte=_now, notification=True).order_by('event_time')
        return games

    @staticmethod
    def one_obj_by_id(id: str):
        return Game.objects.get(id=id)

    @staticmethod
    def get_games_of_team():
        team = Team.objects.filter(type="פומבית")
        _now = datetime.now()
        delta_24_hours = timedelta(hours=24)
        tomorrow = _now + delta_24_hours
        games = Game.objects.filter(team__in=team, event_time__gte=_now, event_time__lte=tomorrow).order_by('event_time')
        return games

    # @staticmethod
    # def get_upcoming_games_24_hours(profile: Profile):




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
    
    @staticmethod
    def get_public_team():
        team = Team.objects.filter(type="פומבית")
        return team
    
    @staticmethod
    def get_count_of_team_for_profile(profile: Profile):
        teams = len(profile.team.all())
        return teams
        

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
            message = AppMessage.objects.filter(team__id=id).order_by('timestamp')[::-1]
        except AppMessage.DoesNotExist as e:
            raise e
        return message

    @staticmethod
    def get_message_by_id(id):
        try:
            message = AppMessage.objects.get(pk=id)
        except AppMessage.DoesNotExist as e:
            raise e
        return message

class AttendanceSelector:
    
    @staticmethod
    def get_obj_by_profile_and_game(profile, game):
        try:
            attendance: Attendance = Attendance.objects.get(profile=profile, game=game)
        except Attendance.DoesNotExist as e:
            game_obj = GameSelector.one_obj_by_id(game)
            attendance: Attendance = db_updater.AttendanceUpdater.create_attendance(profile, game_obj, None)
        return attendance

    @staticmethod
    def get_attendances_by_filter_of_gameId(game: Game):
        attendances = Attendance.objects.filter(game=game, status="מגיע")
        return attendances

class NotificationSelector:

    @staticmethod
    def send_notification_to_members_team_when_open_game(team: Team):
        for profile in team.members.all():
            db_updater.NotificationUpdater.create_new_notification(
                profile=profile, message="נפתח משחק עבורך בקבוצה {}".format(team.name))

    @staticmethod
    def send_notification_to_profile_when_game_in_range_24_hours(profile: Profile, game: Game):
        db_updater.NotificationUpdater.create_new_notification(
            profile=profile, message="יש לך משחק ב{} {} במיקום: {}".format(game.event_time.date(), game.event_time.time() , game.location.name))
    
    def get_notification_by_profile(profile: Profile):
        notification = Notification.objects.filter(profile=profile).order_by('timestamp')[::-1]
        return notification

    def get_notifications_by_profile_and_is_seen(profile: Profile):
        notifications = Notification.objects.filter(profile=profile, is_seen=False)
        return notifications