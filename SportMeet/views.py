from copy import error
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.models import Game
from SportMeet.serializers import GameSerializer, ProfileSerializer, TeamSerializer, UserSerializer
from SportMeet import db_updater, selectors
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout


class ListProfilesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username=None, *args, **kwargs):
        if not username:
            profiles = selectors.ProfileSelector.all_objects()
            serializer = ProfileSerializer(profiles, many=True)
            profiles_data = serializer.data
            return Response(data=profiles_data, status=status.HTTP_200_OK)
        else:
            profile = selectors.ProfileSelector.get_details_profile(username)
            serializer = ProfileSerializer(profile)
            profiles_data = serializer.data
            return Response(data=profiles_data, status=status.HTTP_200_OK)


class ListUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = selectors.UserSelector.all_users()
        serializer = UserSerializer(users, many=True)
        users_data = serializer.data
        return Response(data=users_data, status=status.HTTP_200_OK)


class LoginView(APIView):
    # authentication_classes = []
    # permission_classes = []

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
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)
        if user_serializer.is_valid():
            user = db_updater.UserUpdater.create_new_user(
                data=user_serializer.validated_data)
            if profile_serializer.is_valid():
                db_updater.ProfileUpdater.create_new_profile_for_user(
                    user, profile_serializer.validated_data)
            try:
                profile_data = profile_serializer.validated_data
            except Exception as e:
                profile_data = None
            return Response(data={'user': user_serializer.validated_data, 'profile': profile_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': f'{user_serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


class RecentGamesView(APIView):

    def get(self, request, username, *args, **kwargs):
        games = selectors.GameSelector.three_obj_in_the_future_by_username(
            username)
        game_serializer: GameSerializer = GameSerializer(games, many=True)
        return Response(data={'games': game_serializer.data}, status=status.HTTP_200_OK)


class TeamsView(APIView):

    def get(self, request, username, *args, **kwargs):
        teams = selectors.TeamSelector.three_obj_by_username(username)
        team_serializer: TeamSerializer = TeamSerializer(teams, many=True)
        return Response(data={'teams': team_serializer.data}, status=status.HTTP_200_OK)

class AllTeamsView(APIView):

    def get(self, request, username, *args, **kwargs):
        teams = selectors.TeamSelector.all_obj_by_username(username)
        team_serializer: TeamSerializer = TeamSerializer(teams, many=True)
        return Response(data={'teams' : team_serializer.data}, status=status.HTTP_200_OK)

class ListGamesView(APIView):

    def get(self, request, username, *args, **kwargs):
        games = selectors.GameSelector.many_obj_in_the_future_by_username(
            username)
        game_serializer: GameSerializer = GameSerializer(games, many=True)
        return Response(data={'games': game_serializer.data}, status=status.HTTP_200_OK)

class DetailGameView(APIView):

    def get(self, request, id, *args, **kwargs):
        try:
            game = selectors.GameSelector.one_obj_by_id(id)
            game_serializer: GameSerializer = GameSerializer(game)
            return Response(data={'game': game_serializer.data}, status=status.HTTP_200_OK)
        except Game.DoesNotExist as e:
            return Response(data={"error": "error, user does not exist"}, status=status.HTTP_404_NOT_FOUND)
