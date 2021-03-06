# -*- coding: utf-8 -*-#
from django.conf import settings
from django.db import models

class Users(models.Model):
    MODERATOR = "moderator"
    USER = "user"

    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
    )

    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    activated = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)

    refresh_token = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)

    time_create = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

class UserInfo(models.Model):
    verify_status = models.BooleanField(default=False)
    email = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
