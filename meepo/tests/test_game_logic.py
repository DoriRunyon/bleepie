from __future__ import unicode_literals

from django.test import TestCase

from meepo.models import User, Pet, BAL
from test_models import create_user, create_pet
from meepo.game_logic import *
from django.utils import timezone
from datetime import timedelta

HEALTHY_RANGE_BAL = 0.02
HIGHER_PREVIOUS_BAL = 0.03
LOWER_PREVIOUS_BAL = 0.01
SICK_RANGE_BAL = 0.11
DEAD_RANGE_BAL = 0.16

def create_bal(user, value):

    bal = BAL(user=user, value=value)
    bal.save()

    return bal

class GameLogicTests(TestCase):

    def test_zero_bal_pet_sick(self):

    	bal = 0
    	user = create_user()
    	pet = create_pet(user)
    	pet.health = 'S'
    	pet.save()

    	response = handle_zero_BAL(bal, pet)

    	self.assertEqual(pet.health, 'H')
    	self.assertEqual(response, responses['zero_bal_pet_sick'])

    def test_zero_bal_pet_healthy(self):

    	bal = 0
    	user = create_user()
    	pet = create_pet(user)

    	response = handle_zero_BAL(bal, pet)

    	self.assertEqual(response, responses['zero_bal_pet_healthy'])

    def test_healthy_range_bal_user_not_on_watch(self):

    	user = create_user()
    	pet = create_pet(user)

    	self.assertFalse(user.on_watch)

    	response = handle_healthy_range_BAL(HEALTHY_RANGE_BAL, user, pet, LOWER_PREVIOUS_BAL)

    	self.assertEqual(response, responses['healthy_range_bal_user_off_watch'])
    	self.assertTrue(user.on_watch)

    def test_healthy_range_bal_user_on_watch_and_previous_bal_higher(self):

    	user = create_user()
    	pet = create_pet(user)

    	user.user_on_watch()

    	response = handle_healthy_range_BAL(HEALTHY_RANGE_BAL, user, pet, HIGHER_PREVIOUS_BAL)

    	self.assertEqual(response, responses['healthy_range_bal_user_on_watch_and_higher_previous'])
    	self.assertFalse(user.on_watch)

    def test_healthy_range_bal_user_on_watch_and_previous_bal_lower(self):

    	user = create_user()
    	pet = create_pet(user)

    	user.user_on_watch()

    	response = handle_healthy_range_BAL(HEALTHY_RANGE_BAL, user, pet, LOWER_PREVIOUS_BAL)

    	self.assertEqual(response, responses['healthy_range_bal_user_on_watch_and_lower_previous'])
    	self.assertTrue(user.on_watch)

    def test_sick_range_bal_and_pet_is_healthy(self):

    	user = create_user()
    	pet = create_pet(user)

    	response = handle_sick_range_BAL(SICK_RANGE_BAL, user, pet)

    	self.assertEqual(pet.health, 'S')
    	self.assertEqual(response, responses['sick_range_bal_and_pet_healthy'])
    	self.assertTrue(user.on_watch)

    def test_sick_range_bal_and_pet_is_sick(self):

    	user = create_user()
    	pet = create_pet(user)

    	pet.make_pet_sick()

    	response = handle_sick_range_BAL(SICK_RANGE_BAL, user, pet)

    	self.assertEqual(pet.health, 'S')
    	self.assertEqual(response, responses['sick_range_bal_and_pet_sick'])
    	self.assertTrue(user.on_watch)

    def test_dead_range_bal(self):

    	user = create_user()
    	pet = create_pet(user)

    	live_pets_before = len(Pet.objects.filter(owner=user).exclude(health='D'))
    	response = handle_dead_range_BAL(DEAD_RANGE_BAL, user, pet)
    	live_pets_after = len(Pet.objects.filter(owner=user).exclude(health='D'))

    	self.assertEqual(pet.health, 'D')
    	self.assertEqual(response, responses['dead_range_bal'])
    	self.assertFalse(user.on_watch)
    	self.assertEqual(live_pets_before, 1)
    	self.assertEqual(live_pets_after, 0)

    def test_handle_BAL_pet_healthy_zero_bal(self):

    	user = create_user()
    	pet = create_pet(user)
    	bal = create_bal(user, 0)
    	previous_bal = create_bal(user, 0)

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(response, responses['zero_bal_pet_healthy'])

    def test_handle_BAL_pet_sick_zero_bal(self):

    	user = create_user()
    	pet = create_pet(user)
    	pet.make_pet_sick()
    	bal = create_bal(user, 0)
    	previous_bal = create_bal(user, 0)

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(pet.health, 'H')
    	self.assertEqual(response, responses['zero_bal_pet_sick'])

    def test_handle_BAL_healthy_range_bal_and_user_not_on_watch_and_pet_healthy(self):

    	user = create_user()
    	pet = create_pet(user)
    	bal = create_bal(user, HEALTHY_RANGE_BAL)
    	previous_bal = create_bal(user, 0)

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(response, responses['healthy_range_bal_user_off_watch'])
    	self.assertTrue(user.on_watch)

    def test_handle_BAL_healthy_range_bal_and_user_on_watch_and_previous_bal_lower(self):

    	user = create_user()
    	user.user_on_watch()
    	pet = create_pet(user)
    	bal = create_bal(user, HEALTHY_RANGE_BAL)
    	previous_bal = create_bal(user, LOWER_PREVIOUS_BAL)

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(response, responses['healthy_range_bal_user_on_watch_and_lower_previous'])
    	self.assertTrue(user.on_watch)

    def test_handle_BAL_healthy_range_bal_and_user_on_watch_and_previous_bal_higher(self):

    	user = create_user()
    	user.user_on_watch()
    	pet = create_pet(user)
    	bal = create_bal(user, HEALTHY_RANGE_BAL)
    	previous_bal = create_bal(user, HIGHER_PREVIOUS_BAL)

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(response, responses['healthy_range_bal_user_on_watch_and_higher_previous'])
    	self.assertFalse(user.on_watch)

    def test_handle_BAL_sick_range_bal_and_pet_sick_for_over_24_hours(self):

    	user = create_user()
    	pet = create_pet(user)
    	bal = create_bal(user, SICK_RANGE_BAL)
    	previous_bal = create_bal(user, 0)

    	pet.health = 'S'
    	pet.sick_date = timezone.now() - timedelta(days=2)
    	pet.save()

    	response = handle_BAL(bal, user, pet, previous_bal)

    	self.assertEqual(response, responses['dead_range_bal'])
    	self.assertFalse(user.on_watch)
    	self.assertEqual(pet.health, 'D')

