from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, mobile, password, **extra_fields):
        # if not username:
        #raise ValueError("username is required!!!")
        if not email:
            raise ValueError("email is required!!!")
        if not mobile:
            raise ValueError("mobile is required!!!")

        email = self.normalize_email(email)
        #username = self.model.normalize_username(username)
        user = self.model(email=email,
                          mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, mobile, password, **extra_fields)
