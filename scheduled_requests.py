import os
import django

import mysite.settings

os.environ.setdefault(
		"DJANGO_SETTINGS_MODULE",
		"mysite.settings"
)

django.setup()

from meepo.models import User, Pet
from meepo.views import request_BAL


#run this at 9pm Pacific time
def first_BAL_requests():
    """Make first request to all users."""

    pets = Pet.objects.exclude(health='D')

    for pet in pets:
        owner = pet.owner
        phone_number = owner.phone_number
        request_BAL(phone_number)


#run this at 10pm and 11pm Pacific time
def subsequent_BAL_requests():
    """Make second request to all users."""

    users = User.objects.filter(on_watch=True)

    for user in users:
        request_BAL(user.phone_number)

#run this at midnight Pacific time
def all_users_off_watch():
    """Run daily at midnight."""

    users = User.objects.filter(on_watch=True)

    for user in users:
        user.user_off_watch()
