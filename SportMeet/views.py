from copy import error
from re import A, sub
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.template import TemplateDoesNotExist
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.models import AppMessage, Attendance, Game, GameField, Profile, Team
from SportMeet.serializers import AppMessageSerializer, AttendanceSerializer, GameSerializer, NotificationSerializer, ProfileSerializer, TeamSerializer, UserSerializer, GameFieldSerializer, CitySerializer
from SportMeet import db_updater, selectors
from rest_framework.permissions import AllowAny, IsAuthenticated
import csv
from django.contrib.auth import authenticate, login, logout


class ListProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None, *args, **kwargs):
        if not username:
            profiles = selectors.ProfileSelector.all_objects()
            serializer = ProfileSerializer(profiles, many=True)
            profiles_data = serializer.data
            return Response(data=profiles_data, status=status.HTTP_200_OK)
        else:
            # breakpoint()
            profile = selectors.ProfileSelector.get_details_profile(username)
            serializer = ProfileSerializer(profile)
            profiles_data = serializer.data
            return Response(data=profiles_data, status=status.HTTP_200_OK)

    def put(self, request, username, *args, **kwargs):
        email = request.data['email']
        city = request.data['city']
        age = request.data['age']
        sex = request.data['sex']
        profile = selectors.ProfileSelector.get_details_profile(username)
        profile.email = email
        profile.city = city
        profile.age = age
        profile.sex = sex
        update_profile = db_updater.ProfileUpdater.update_deailts_profile(
            profile)
        serializer = ProfileSerializer(update_profile)
        try:
            profiles_data = serializer.data
            return Response(data=profiles_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'errors': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDataView(APIView):
    def get(self, request, username, *args, **kwargs):
        profile = selectors.ProfileSelector.get_details_profile(username)
        count = selectors.TeamSelector.get_count_of_unanonymous_team_for_profile(
            profile)
        count_attendance_game = selectors.GameSelector.count_of_games_in_the_feuture(
            profile)
        return Response(data={'teams': count, 'games': count_attendance_game}, status=status.HTTP_200_OK)


class ListUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = selectors.UserSelector.all_users()
        serializer = UserSerializer(users, many=True)
        users_data = serializer.data
        return Response(data=users_data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None or password is None:
            return Response(data={'error': 'Missing username or password keywords in request data'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status.HTTP_200_OK)
        return Response(data={'error': 'bad credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)
        profile_serializer.is_valid()
        if user_serializer.is_valid():
            user = db_updater.UserUpdater.create_new_user(
                data=user_serializer.data)
            profile = db_updater.ProfileUpdater.create_new_profile_for_user(
                user, profile_serializer.data)
            try:
                profile_data = ProfileSerializer(profile).data
                # print(profile_data)
                # print('+++++++++++++++++++++++++++++')
                # profile_data['email'] = Profile.decrypt_and_decode_email(
                #     profile_data['email'])
                print(profile_data)
            except Exception as e:
                profile_data = None
            return Response(data={'user': user_serializer.validated_data, 'profile': profile_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': f'{user_serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


class CreateTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        name = request.data['name']
        sport = request.data['sport']
        type = request.data['type']
        admin = request.user.profile
        members = [request.user.profile]
        try:
            team = db_updater.TeamUpdater.create_new_team(
                admin=admin, members=members, sport=sport, name=name, type=type)
            return Response(data={'team': TeamSerializer(team).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'errors': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrEditTeamView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data['id']
        try:
            db_updater.TeamUpdater.delete_team_by_id(id)
            return Response(status=status.HTTP_200_OK)
        except TemplateDoesNotExist as e:
            return Response(data={'errors': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        team = selectors.TeamSelector.get_obj_by_id(id)
        team.name = request.data['name']
        team.sport = request.data['sport']
        team.type = request.data['type']
        team_updated = db_updater.TeamUpdater.update_details_team(team)
        return Response(data={"team": TeamSerializer(team_updated).data}, status=status.HTTP_200_OK)


class CreateNewGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            team = selectors.TeamSelector.get_obj_by_id(request.data["team"])
        except:
            team = db_updater.TeamUpdater.create_new_team(sport=request.data["type"],
                                                          name=uuid.uuid1(), admin=request.user.profile,
                                                          anonymous=True, members=[request.user.profile], type=request.data["typeTeam"])
        try:
            location = selectors.GameFieldSelector.get_game_field_by_id(
                request.data["location"])
        except:
            location = None
        try:
            date = request.data["date"].replace(
                ".", "-") + " " + request.data["time"]
            event_time = datetime.strptime(date, '%d-%m-%Y %H:%M')
        except ValueError as e:
            date = datetime.strptime(
                request.data['date'], '%a %b %d %H:%M:%S %Y').strftime('%d-%m-%Y %H:%M')
            event_time = datetime.strptime(date, '%d-%m-%Y %H:%M')
        limit_participants = request.data['limitParticipants']
        if not selectors.GameSelector.check_if_exist_game(event_time, location):
            return Response(data={"error": "existing game in same location and event time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        game = db_updater.GameUpdater.create_new_game(
            team=team, location=location, event_time=event_time, limit_participants=limit_participants)
        if request.data["team"]:
            selectors.NotificationSelector.send_notification_to_members_team_when_open_game(
                team)
        try:
            return Response(data={'game': GameSerializer(game).data, 'team': TeamSerializer(team).data,
                                  'location': GameFieldSerializer(location).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class RecentGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        games = selectors.GameSelector.three_obj_in_the_future_by_username(
            username)
        game_serializer: GameSerializer = GameSerializer(games, many=True)
        upcoming_games = selectors.GameSelector.all_upcoming_games(username)
        _now = timezone.now()
        delta_24_hours = timedelta(hours=24)
        tomorrow = _now + delta_24_hours
        profile = selectors.ProfileSelector.get_details_profile(username)
        for game in upcoming_games:
            if game.event_time > _now and game.event_time < tomorrow:
                selectors.NotificationSelector.send_notification_to_profile_when_game_in_range_24_hours(
                    profile, game)
                game.notification = False
                db_updater.GameUpdater.update_notification_field(game)
        return Response(data={'games': game_serializer.data}, status=status.HTTP_200_OK)


class TeamsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        teams = selectors.TeamSelector.three_obj_by_username(username)
        team_serializer: TeamSerializer = TeamSerializer(teams, many=True)
        return Response(data={'teams': team_serializer.data}, status=status.HTTP_200_OK)


class TeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        team = selectors.TeamSelector.get_obj_by_id(id)
        team_serializer: TeamSerializer = TeamSerializer(team)
        return Response(data={'team': team_serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        team = selectors.TeamSelector.get_obj_by_id(id)
        profile = selectors.ProfileSelector.get_profile_by_id(
            request.data['profileId'])
        team.members.add(profile)
        selectors.NotificationSelector.send_notification_when_profile_added_to_team(
            profile, team)
        team_update = db_updater.TeamUpdater.update_details_team(team)
        team_serializer: TeamSerializer = TeamSerializer(team_update)
        return Response(data={'team': team_serializer.data}, status=status.HTTP_200_OK)


class AllTeamsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        teams = selectors.TeamSelector.all_obj_by_username(username)
        team_serializer: TeamSerializer = TeamSerializer(teams, many=True)
        return Response(data={'teams': team_serializer.data}, status=status.HTTP_200_OK)


class ListGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        games = selectors.GameSelector.many_obj_in_the_future_by_username(
            username)
        game_serializer: GameSerializer = GameSerializer(games, many=True)
        return Response(data={'games': game_serializer.data}, status=status.HTTP_200_OK)


class DetailGameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            game = selectors.GameSelector.one_obj_by_id(id)
            game_serializer: GameSerializer = GameSerializer(game)
            return Response(data={'game': game_serializer.data}, status=status.HTTP_200_OK)
        except Game.DoesNotExist as e:
            return Response(data={"error": "error, user does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, *args, **kwargs):
        try:
            game = selectors.GameSelector.one_obj_by_id(id)
            game.limit_participants = request.data['limitParticipants']
            game.location = selectors.GameFieldSelector.get_game_field_by_id(
                request.data['location'])

            game = db_updater.GameUpdater.update_game_details(game)
            game_serializer: GameSerializer = GameSerializer(game)
            return Response(data={'game': game_serializer.data}, status=status.HTTP_200_OK)
        except Game.DoesNotExist as e:
            return Response(data={"error": "error, user does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, *args, **kwargs):
        game = db_updater.GameUpdater.delete_game_by_id(id)
        if game:
            return Response(data={'message': 'The game was deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': "The game does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class GameFieldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        game_field = selectors.GameFieldSelector.all_game_field()
        game_field_serializer: GameFieldSerializer = GameFieldSerializer(
            game_field, many=True)
        return Response(data={'locations': game_field_serializer.data}, status=status.HTTP_200_OK)


class AppMessageView(APIView):
    permissions_class = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        messages = selectors.AppMessageSelector.get_message_by_team_id(id)
        messages_serializer: AppMessageSerializer = AppMessageSerializer(
            messages, many=True)
        return Response(data={"messages": messages_serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        message = selectors.AppMessageSelector.get_message_by_id(id)
        seen = request.data['seen']
        message.seen = seen
        update_message = db_updater.AppMessageUpdater.change_seen_for_messgae(
            message=message)
        serializer = AppMessageSerializer(update_message)
        try:
            message_data = serializer.data
            return Response(data=message_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'errors': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, teamID, *args, **kwargs):
        sender = request.user.profile
        #sender = selectors.ProfileSelector.get_details_profile('admin')
        try:
            team = selectors.TeamSelector.get_obj_by_id(teamID)
        except Team.DoesNotExist as e:
            return Response(data={'errors': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        timestamp = datetime.now()
        subject = request.data['subject']
        body = request.data['body']
        new_msg = db_updater.AppMessageUpdater.post_message(
            sender, subject, body, timestamp, team)
        try:
            return Response(data={'message': AppMessageSerializer(new_msg).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': f'{repr(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, messageId, *args, **kwargs):
        message = db_updater.AppMessageUpdater.delete_message_by_id(messageId)
        if message:
            return Response(data={'message': 'The message was deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': "The messgae does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class ImportData(APIView):
    def get(self, request, *args, **kwargs):
        file = open('Game Field Data.csv', 'r', newline='', encoding='UTF8')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            is_for_football = False
            is_for_basketball = False
            is_for_tennis = False
            payment = False
            if not 'לא תקני' in row[3] and not 'ביה"ס' in row[4] and not 'בית ספר' in row[4] and not 'בי"ס' in row[4] and not 'לא' in row[21] and not 'בריכ' in row[3] and not 'כושר' in row[3] and not 'לא תקני' in row[3] and not 'ליג' in row[23] and not 'מסלול' in row[3] and not 'אקסטרים' in row[3] and not 'חול' in row[3] and not 'שייט' in row[3] and not 'מוטורי' in row[3]:
                if 'כדורגל' in row[3] or 'מיני' in row[3] or 'שחבק' in row[3] or 'משולב' in row[3] or 'קט רגל' in row[3]:
                    is_for_football = True
                if 'כדורסל' in row[3] or 'משולב' in row[3]:
                    is_for_basketball = True
                if 'טניס' in row[3]:
                    is_for_tennis = True
                if 'תיאום' in row[16] or 'תשלום' in row[16]:
                    payment = True
                db_updater.GameFieldUpdater.create_new_field_game(name=row[4],
                                                                  street=row[6], region=row[0], address_number=row[
                                                                      7], availability=row[16], is_for_football=is_for_football,
                                                                  is_for_basketball=is_for_basketball, is_for_tennis=is_for_tennis, telephone=row[13], payment=payment)
        return Response(data={"Message": "Done"}, status=status.HTTP_201_CREATED)
    # add response to get function


class importCityView(APIView):
    def get(self, request, city, *args, **kwargs):
        game_filed_list = selectors.DataSelector.get_all_game_field_by_city_name(
            city)
        return Response(data=GameFieldSerializer(game_filed_list, many=True).data, status=status.HTTP_200_OK)


class importGameFiledByCityView(APIView):
    def get(self, request, city, typeSport, *args, **kwargs):
        game_filed_list = selectors.DataSelector.get_all_game_field_by_city_name_and_type_sport(
            city, typeSport)
        return Response(data=GameFieldSerializer(game_filed_list, many=True).data, status=status.HTTP_200_OK)


class AttendanceView(APIView):
    def put(self, request, username, *args, **kwargs):
        attendance = int(request.data['index'])
        if attendance == 0:
            attendance = 'מגיע'
        elif attendance == 1:
            attendance = 'לא מגיע'
        elif attendance == 2:
            attendance = 'אולי מגיע'
        profile = selectors.ProfileSelector.get_details_profile(username)
        game = selectors.GameSelector.one_obj_by_id(request.data['game'])
        try:
            obj = selectors.AttendanceSelector.get_obj_by_profile_and_game(
                profile, game)
            obj.status = attendance
            obj = db_updater.AttendanceUpdater.change_attendance(obj)
        except Attendance.DoesNotExist:
            obj = db_updater.AttendanceUpdater.create_attendance(
                profile, game, attendance)
        return Response(data={'attendance': AttendanceSerializer(obj).data}, status=status.HTTP_201_CREATED)

    def get(self, request, username, game, *args, **kwargs):
        profile = selectors.ProfileSelector.get_details_profile(username)
        obj = selectors.AttendanceSelector.get_obj_by_profile_and_game(
            profile, game)
        return Response(data={'attendance': AttendanceSerializer(obj).data}, status=status.HTTP_200_OK)


class AttendancesStatusView(APIView):
    def get(self, request, gameId, *args, **kwargs):
        game = selectors.GameSelector.one_obj_by_id(gameId)
        attendances = selectors.AttendanceSelector.get_attendances_by_filter_of_gameId(
            game)
        return Response(data={'attendance': AttendanceSerializer(attendances, many=True).data}, status=status.HTTP_200_OK)


class PublicGamesView(APIView):
    def get(self, request, *args, **kwargs):
        games = selectors.GameSelector.get_games_of_team()
        serializer = GameSerializer(games, many=True)
        games_serializer = serializer.data
        return Response(data={'games': games_serializer}, status=status.HTTP_200_OK)


class NotificationView(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            profile = selectors.ProfileSelector.get_details_profile(username)
        except Profile.DoesNotExist as e:
            return Response(data={"message": "Username does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        notification = selectors.NotificationSelector.get_notification_by_profile(
            profile)
        return Response(data={"notification": NotificationSerializer(notification, many=True).data}, status=status.HTTP_200_OK)

    def put(self, request, username, *args, **kwargs):
        try:
            profile = selectors.ProfileSelector.get_details_profile(username)
        except Profile.DoesNotExist as e:
            return Response(data={"message": "Username does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        notifications = selectors.NotificationSelector.get_notifications_by_profile_and_is_seen(
            profile)
        for notification in notifications:
            notification.is_seen = True
            db_updater.NotificationUpdater.update_is_seen_field_to_true(
                notification)
        return Response(data={"message": "All notification is changed"}, status=status.HTTP_200_OK)


class NotificationAmountView(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            profile = selectors.ProfileSelector.get_details_profile(username)
        except Profile.DoesNotExist as e:
            return Response(data={"message": "Username does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        notification = selectors.NotificationSelector.get_notifications_by_profile_and_is_seen(
            profile)
        return Response(data={"Amount of unseen notifications": len(notification)}, status=status.HTTP_200_OK)

class ImportCitiesView(APIView):
    def get(self, request, *args, **kwargs):
        cities = selectors.CitySelector.add_cities()
        if cities == "done":
            return Response(data={"message": "done"}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Error"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ConvertCityView(APIView):
    def get(self, request, city, *args, **kwargs):
        city = selectors.CitySelector.find_city_by_name(city)
        if city:
            return Response(data={"city": CitySerializer(city).data}, status=status.HTTP_200_OK)
        else: 
            return Response(data={"message": "City does not exist"})