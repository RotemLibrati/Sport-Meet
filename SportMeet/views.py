from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.serializers import ProfileSerializer, UserSerializer
from SportMeet import db_updater, selectors
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout


class ListProfilesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        profiles = selectors.ProfileSelector.all_objects()
        serializer = ProfileSerializer(profiles, many=True)
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
    authentication_classes = []
    permission_classes = []

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
                data=user_serializer.data)
            if profile_serializer.is_valid():
                db_updater.ProfileUpdater.create_new_profile_for_user(
                    user, profile_serializer.data)
            try:
                profile_data = profile_serializer.data
            except Exception as e:
                profile_data = None
            return Response(data={'user': user_serializer.data, 'profile': profile_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': f'{user_serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
