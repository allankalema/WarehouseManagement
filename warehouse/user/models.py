# user/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, store_name, owner=False, store_manager=False, shop=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            store_name=store_name,
            owner=owner,
            store_manager=store_manager,
            shop=shop
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, store_name, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            store_name=store_name,
            password=password,
            owner=True
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    store_name = models.CharField(max_length=100)
    owner = models.BooleanField(default=False)
    store_manager = models.BooleanField(default=False)
    shop = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'store_name']

    def __str__(self):
        return self.email
