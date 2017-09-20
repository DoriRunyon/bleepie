# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=10)
    on_watch = models.BooleanField(default=False)

    def __str__(self):
        return "User name: %s" % self.username

    def user_on_watch(self):
        self.on_watch = True
        self.save()

    def user_off_watch(self):
        self.on_watch = False
        self.save()

class BAL(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.FloatField()
    time = models.DateTimeField(default=timezone.now)


class Pet(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField("Pet's name", max_length=100)
    born_date = models.DateTimeField(default=timezone.now)
    sick_date = models.DateTimeField(blank=True, null=True)
    death_date = models.DateTimeField(blank=True, null=True)
    HEALTHY = 'H'
    SICK = 'S'
    DEAD = 'D'
    HEALTH_STATUS = (
        ('H', 'Healthy'),
        ('S', 'Sick'),
        ('D', 'Dead'),
    )
    health = models.CharField("Pet's health", max_length=1, choices=HEALTH_STATUS, default=HEALTHY)

    def __str__(self):
        return "Pet name: %s" % self.name

    def make_pet_healthy(self):
        self.health = 'H'
        self.save()

    def make_pet_sick(self):
        self.health = 'S'
        self.sick_date = timezone.now()
        self.save()

    def kill_pet(self):
        self.health = 'D'
        self.death_date = timezone.now()
        self.save()


