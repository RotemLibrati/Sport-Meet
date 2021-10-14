from SportMeet.models import Profile, Team, TeamPrivileges


class ProfileSelector:

    @staticmethod
    def all_objects():
        return Profile.objects.all()
