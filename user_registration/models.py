from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from user_registration.manager import UserManager
from utilities.constants.RoleEnum import UserRole, DEVELOPER


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=50, null=False)
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=2, choices=UserRole, default=DEVELOPER)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name

    class Meta:
        db_table = u'users'
