from SportMeet.models import Profile, Team


class ProfileSelector:

    @staticmethod
    def all_objects():
        return Profile.objects.all()
