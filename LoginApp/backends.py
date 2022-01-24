# Django
from django.contrib.auth.backends import ModelBackend
# Models
from .models import UserModel as User
from django.db.models import Q


class CustomBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        print("in custome aunthenticate : ", email, password)
        try:
            user = User.objects.get(Q(email=email) | Q(mobile=email))
        except User.DoesNotExist:
            return None

        if password is None:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user



