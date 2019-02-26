from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birth = models.DateTimeField(blank=True, default=timezone.now)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return "user {}".format(self.user.username)
