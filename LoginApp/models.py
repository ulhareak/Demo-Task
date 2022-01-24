from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils.translation import gettext_lazy as _
#from django.utils.translation import gettext_lazy as _

# 0from phonenumber_field.model import PhoneNumberField

# Create your models here.


class UserModel(AbstractUser):
    mobile = models.CharField(max_length=10, unique=True, blank=True)
    #username_validator = UnicodeUsernameValidator()
    username = None  # models.CharField(max_length=128 , unique=True ,
    # error_messages={'unique': _("A user with that username already exists.")})
    password = models.CharField(_('password'), max_length=128, blank=True)
    email = models.EmailField(max_length=128, unique=True)
    #role = models.CharField(max_length=50 , null = True )
    role = models.CharField(_('Role'), max_length=255,default='emp',
     blank=True ,choices=[('emp', 'emp'), ('admin', 'admin'), ('hr', 'hr')])

    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'first_name', 'password']

    objects = UserManager()


