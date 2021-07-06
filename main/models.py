from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import timezone


class UserManager(BaseUserManager):
    def create_user(self, name, password=None):
        if not name:
            raise ValueError('Ismingizni kiriting!')
        user = self.model(name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, password):
        user = self.create_user(name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'name'


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(Region, related_name='district', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)

    def __str__(self):
        return self.user.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.name
