from SportMeet.models import Profile, Team
from django.contrib.auth.models import User



class ProfileSelector:

    @staticmethod
    def all_objects():
        return Profile.objects.all()

    @staticmethod
    def one_obj_by_email(email):
        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist as e:
            raise e
        return profile

class UserSelector:
    @staticmethod
    def all_users():
        return User.objects.all()
