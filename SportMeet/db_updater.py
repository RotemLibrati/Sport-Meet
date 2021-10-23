from SportMeet.models import Profile
from SportMeet import selectors


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
