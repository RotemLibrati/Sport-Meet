from SportMeet.models import Profile
from SportMeet import selectors
from django.contrib.auth.models import User


class ProfileUpdater:
    @staticmethod
    def update_user_by_email(email, **kwargs):
        try:
            profile = selectors.ProfileSelector.one_obj_by_email(email)
        except Profile.DoesNotExist as e:
            raise e
        for key, val in kwargs.items():
            setattr(profile, key, val)
        profile.save()

    @staticmethod
    def create_new_profile_for_user(user: User, data: dict):
        profile: Profile = Profile(user=user, **data)
        profile.save()
        return profile


class UserUpdater:
    @staticmethod
    def create_new_user(data: dict):
        _password = data['password']
        del data['password']
        user = User(**data)
        user.set_password(_password)
        user.save()
        return user
