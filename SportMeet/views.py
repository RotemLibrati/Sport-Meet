from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.models import Profile
from SportMeet.serializers import ProfileSerializer

class ListProfilesView(APIView):

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        profiles_data = serializer.data
        return Response(data=profiles_data, status=status.HTTP_200_OK)
