from rest_framework import serializers
from SportMeet.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude = []