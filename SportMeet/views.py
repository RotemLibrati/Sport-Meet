from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportMeet.serializers import ProfileSerializer
from SportMeet import selectors


class ListProfilesView(APIView):

    def get(self, request, *args, **kwargs):
        profiles = selectors.ProfileSelector.all_objects()
        serializer = ProfileSerializer(profiles, many=True)
        profiles_data = serializer.data
        return Response(data=profiles_data, status=status.HTTP_200_OK)
