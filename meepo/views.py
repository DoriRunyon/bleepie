# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#other libraries
import os
from datetime import datetime, date, time

#django 
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .models import Pet, User, BAL
from .forms import PetForm, SignUpForm

from game_logic import handle_BAL


#twilio 
from twilio.rest import Client
from decorators import validate_twilio_request
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(twilio_account_sid, twilio_auth_token)
my_phone_number = os.environ['MY_PHONE']
twilio_phone_number = os.environ['TWILIO_PHONE']

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('pet_status')
    else:
        form = SignUpForm()
    return render(request, 'meepo/signup.html', {'form': form})

@login_required
def pet_status(request):
    pet = Pet.objects.filter(owner=request.user.pk).exclude(health='D')
    days_alive = 0
    pet_health_message = 'Deceased'
    if pet:
        #user has a live pet
        pet = pet[0]
        born_date = pet.born_date.replace(tzinfo=None)
        delta = datetime.now() - born_date
        days_alive = delta.days + 1
        if pet.health == 'H':
            pet_health_message = 'Excellent'
        else:
            pet_health_message = 'Poor'
    else:
        pet = Pet.objects.filter(owner=request.user.pk).order_by('-death_date')
        if not pet:
            #user has no pet, living or dead
            pet = None
        else:
            #user's pet which most recently died is displayed
            pet = pet[0]

    return render(request, 'meepo/pet_status.html', {'pet': pet, 'days_alive': days_alive, 'pet_health_message': pet_health_message})

def about(request): 

    return render(request, 'meepo/about.html')

def contact(request): 

    return render(request, 'meepo/contact.html')

@login_required
def hatch_pet(request):
    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_status')
    else:
        form = PetForm()
    return render(request, 'meepo/hatch_pet.html', {'form': form})

@login_required
def change_pet_health_based_on_BAL(request):
    if request.method == "POST":
        user = request.user
        previous_bal = get_previous_bal(user)
        input_bal = float(request.POST['BAL'])
        bal = BAL(user=user, value=input_bal)
        bal.save()
        pet = Pet.objects.filter(owner=request.user.pk).exclude(health='D')[0]
        handle_BAL(bal, user, pet, previous_bal)

    return redirect('pet_status')

def request_BAL(phone_number):

    message = client.messages.create(to=phone_number, from_=twilio_phone_number, body="Can I have your BAL please?")

    return HttpResponse(message, content_type='text/xml')

@csrf_exempt
@validate_twilio_request
def incoming_sms(request):

    user_phone_number = request.GET['From']
    user_phone_number_db_lookup = request.GET['From'][2:]

    if not user_phone_number_db_lookup:
            handle_sms_received_user_not_found(request.GET['From'])

    try:
        bal = float(request.GET['Body'])
        user = User.objects.filter(phone_number=user_phone_number_db_lookup)[0]
        
        try:
            pet = Pet.objects.filter(owner=user.pk).exclude(health='D')[0]
        except IndexError:
            message = client.messages.create(to=user_phone_number, from_=twilio_phone_number, body="You have no pet! Go to bleepie.herokuapp.com to hatch a Bleepie.")
            return HttpResponse(message, content_type='text/xml')

        previous_bal = get_previous_bal(user)
        bal = save_user_BAL_data(user, bal)
        message_to_user = handle_BAL(bal, user, pet, previous_bal)
        message = client.messages.create(to=user_phone_number, from_=twilio_phone_number, body=message_to_user)

        return HttpResponse(message, content_type='text/xml')

    except ValueError:
        if message_from_user == 'k' or message_from_user == 'K':
            user = User.objects.filter(phone_number=user_phone_number_db_lookup)[0]
            pet = Pet.objects.filter(owner=user.pk).exclude(health='D')[0]
            pet.kill_pet()
        else:
            handle_incorrect_input(request.GET['From'])


def handle_incorrect_input(phone_number):

    message = client.messages.create(to=phone_number, 
                                    from_=twilio_phone_number, 
                                    body="That didn't make sense - please send a BAL, thank you! Or text 'K' or 'k' to kill your pet and no longer receive messages.")

    return HttpResponse(message, content_type='text/xml')

def handle_sms_received_user_not_found(phone_number):

    message = client.messages.create(to=phone_number, from_=twilio_phone_number, body="I don't recognize your number! Please go to ??? and create an account :)")

    return HttpResponse(message, content_type='text/xml')

def get_previous_bal(user):

    try:
        previous_bal = BAL.objects.filter(user=user.pk).order_by('-id')[0]
    except IndexError:
        previous_bal = 0

    return previous_bal

def save_user_BAL_data(user, bal):

    bal_object = BAL(user=user, value=bal)
    bal_object.save()

    return bal_object
