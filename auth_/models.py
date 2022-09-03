import datetime
import time

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        user = self.create_user(username, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # an admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    objects = UserManager()
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Email &amp; Password are required by default.

    def get_full_name(self):
        return self.name + " " + self.surname

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.get_username()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
