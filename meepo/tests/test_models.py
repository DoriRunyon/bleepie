# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from meepo.models import User, Pet, BAL

def create_user():

    owner = User(username="test_user")
    owner.save()

    return owner

def create_pet(user):

	pet = Pet(owner=user, name="test_pet")
	pet.save()

	return pet

class PetModelTests(TestCase):

    def test_make_pet_healthy(self):

        user = create_user()
    	pet = create_pet(user)
    	pet.health = 'S'
    	pet.save()
    	pet.make_pet_healthy()

    	self.assertTrue(pet.health, 'H')

    def test_make_pet_sick(self):

        user = create_user()
    	pet = create_pet(user)
    	pet.make_pet_sick()

    	self.assertTrue(pet.health, 'S')

    def test_kill_pet(self):

        user = create_user()
    	pet = create_pet(user)
    	pet.kill_pet()

    	self.assertTrue(pet.health, 'D')

    
