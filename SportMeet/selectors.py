from datetime import time, tzinfo
from operator import le
from os import stat
import profile
import requests
from django.forms import DateTimeField
from SportMeet.models import AppMessage, Attendance, GameField, Notification, Profile, Team, Game, City
from django.contrib.auth.models import User
from SportMeet import db_updater
from datetime import datetime, timedelta
from django.utils import timezone
import os
from django.core.mail import EmailMessage


class ProfileSelector:

    @staticmethod
    def all_objects():
        return Profile.objects.all()

    @staticmethod
    def one_obj_by_email(email):
        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist as e:
            return e
        return profile

    @staticmethod
    def get_details_profile(username):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        return profile

    @staticmethod
    def get_profile_by_id(id):
        profile = Profile.objects.get(id=id)
        return profile


class UserSelector:
    @staticmethod
    def all_users():
        return User.objects.all()
    
    def get_user_by_profile(profile: Profile):
        return User.objects.get(profile=profile)


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
    def count_of_games_in_the_feuture(profile: Profile):
        games = Attendance.objects.filter(profile=profile, status="מגיע")
        return len(games)

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
        games = Game.objects.filter(
            team__in=team, event_time__gte=_now, event_time__lte=tomorrow).order_by('event_time')
        return games

    @staticmethod
    def check_if_exist_game(event_time: datetime, location: GameField):
        games = Game.objects.filter(location=location)
        for game in games:
            if game.event_time.date() == event_time.date():
                if game.event_time.time().hour+3 - event_time.time().hour <= 2 and game.event_time.time().hour+3 - event_time.time().hour > -2:
                    return False
        return True

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
    def get_count_of_unanonymous_team_for_profile(profile: Profile):
        teams = profile.team.all()
        count = 0

        for team in teams:
            if team.anonymous != True:
                count += 1
        # unanonymous_team
        return count


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
            message = AppMessage.objects.filter(
                team__id=id).order_by('timestamp')[::-1]
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
            attendance: Attendance = Attendance.objects.get(
                profile=profile, game=game)
        except Attendance.DoesNotExist as e:
            game_obj = GameSelector.one_obj_by_id(game)
            attendance: Attendance = db_updater.AttendanceUpdater.create_attendance(
                profile, game_obj, None)
        return attendance

    @staticmethod
    def get_attendances_by_filter_of_gameId(game: Game):
        attendances = Attendance.objects.filter(game=game, status="מגיע")
        return attendances


class NotificationSelector:

    @staticmethod
    def send_notification_to_members_team_when_open_game(team: Team):
        for profile in team.members.all():
            if team.anonymous:
                db_updater.NotificationUpdater.create_new_notification(
                    profile=profile, message="נפתח משחק עבורך בקבוצה")
            else:
                db_updater.NotificationUpdater.create_new_notification(
                    profile=profile, message="נפתח משחק עבורך בקבוצה {}".format(team.name))

    @staticmethod
    def send_notification_to_profile_when_game_in_range_24_hours(profile: Profile, game: Game):
        db_updater.NotificationUpdater.create_new_notification(
            profile=profile, message="יש לך משחק ב{} {} במיקום: {}".format(game.event_time.date(), game.event_time.time(), game.location.name))

    @staticmethod
    def send_notification_when_profile_added_to_team(profile: Profile, team: Team):
        db_updater.NotificationUpdater.create_new_notification(
            profile=profile, message="{} הוסיף אותך לקבוצת {}".format(team.admin, team.name))

    def get_notification_by_profile(profile: Profile):
        _now = datetime.now()
        delta_96_hours = timedelta(hours=-96)
        new_date = _now + delta_96_hours
        notification = Notification.objects.filter(
            profile=profile, timestamp__gte=new_date).order_by('timestamp')[::-1]
        return notification

    def get_notifications_by_profile_and_is_seen(profile: Profile):
        notifications = Notification.objects.filter(
            profile=profile, is_seen=False)
        return notifications


class EmailSelector:
    @staticmethod
    def send_message(reciver, subject, body):
        print(type(reciver))
        email = EmailMessage(
            subject,
            body,
            'sportmeetsce@gmail.com',
            [reciver]
        )
        email.send()


class DataSelector:

    @staticmethod
    def get_all_game_field_by_city_name(city_name: str):
        city = GameField.objects.filter(region=city_name)
        return city

    @staticmethod
    def get_all_game_field_by_city_name_and_type_sport(city_name: str, typeSport: str):
        if typeSport == 'כדורגל':
            city = GameField.objects.filter(
                region=city_name, is_for_football=True)
        elif typeSport == 'כדורסל':
            city = GameField.objects.filter(
                region=city_name, is_for_basketball=True)
        elif typeSport == 'טניס':
            city = GameField.objects.filter(
                region=city_name, is_for_tennis=True)
        return city


class CitySelector:
    @staticmethod
    def add_cities():
        db_updater.ImportCitiesUpdater.add_cities_to_db("ירושלים", "Jerusalem")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "באר שבע", "Be'er Sheva")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "מצפה רמון", "Mizpe Ramon")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "תל אביב-יפו", "Tel Aviv-Yafo")
        db_updater.ImportCitiesUpdater.add_cities_to_db("אופקים", "Ofakim")
        db_updater.ImportCitiesUpdater.add_cities_to_db("חיפה", "Haifa")
        db_updater.ImportCitiesUpdater.add_cities_to_db("רמת גן", "Ramat Gan")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "ראשון לציון", "Rishon Letsiyon")
        db_updater.ImportCitiesUpdater.add_cities_to_db("אשדוד", "Ashdod")
        db_updater.ImportCitiesUpdater.add_cities_to_db("נתניה", "Natanya")
        db_updater.ImportCitiesUpdater.add_cities_to_db("הרצליה", "Herzliya")
        db_updater.ImportCitiesUpdater.add_cities_to_db("כפר סבא", "Kfar Saba")
        db_updater.ImportCitiesUpdater.add_cities_to_db("חדרה", "Hadera")
        db_updater.ImportCitiesUpdater.add_cities_to_db("בת ים", "Bat Yam")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "גבעתיים", "Givat Haim")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "קרית גת", "Qiryat Gat")
        db_updater.ImportCitiesUpdater.add_cities_to_db("נהריה", "Nahariya")
        db_updater.ImportCitiesUpdater.add_cities_to_db("יבנה", "Yavne")
        db_updater.ImportCitiesUpdater.add_cities_to_db("אילת", "Eilat")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "רמת השרון", "Ramat Hasharon")
        db_updater.ImportCitiesUpdater.add_cities_to_db("טבריה", "Tiberias")
        db_updater.ImportCitiesUpdater.add_cities_to_db("נתיבות", "Netivot")
        db_updater.ImportCitiesUpdater.add_cities_to_db("דימונה", "Dimona")
        db_updater.ImportCitiesUpdater.add_cities_to_db("שדרות", "Sderot")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "קרית שמונה", "Qiryat Shmona")
        db_updater.ImportCitiesUpdater.add_cities_to_db("ירוחם", "Yeruham")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "קרית מוצקין", "Qiryat Motzkin")
        db_updater.ImportCitiesUpdater.add_cities_to_db(
            "בית שמש", "Beit-Shemesh")
        return "done"

    def find_city_by_name(city: str):
        try:
            converted_city = City.objects.get(hebrew_name=city)
            return converted_city
        except City.DoesNotExist as e:
            return False
