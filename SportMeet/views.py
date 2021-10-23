from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.serializers import ProfileSerializer
from SportMeet import selectors
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout




class ListProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = selectors.ProfileSelector.all_objects()
        serializer = ProfileSerializer(profiles, many=True)
        profiles_data = serializer.data
        return Response(data=profiles_data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

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
