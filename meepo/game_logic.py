from datetime import datetime, date, time
from django.utils import timezone

responses = {
        'zero_bal_pet_healthy': "Good jorb!",
        'zero_bal_pet_sick': "Your bleepie is recovered.",
        'healthy_range_bal_user_off_watch': "OK for now but we'll keep our eye on you.",
        'healthy_range_bal_user_on_watch_and_lower_previous': "OK for now but we'll keep our eye on you.",
        'healthy_range_bal_user_on_watch_and_higher_previous': "Drink some water and get some rest!",
        'sick_range_bal_and_pet_healthy': "Watch out - your bleepie is mighty sick.",
        'sick_range_bal_and_pet_sick': "Your bleepie is already sickly :(",
        'dead_range_bal': "You killed your bleepie! Go to ??? to hatch a new bleepie pet :("

}

SICK_BAL = float(0.10)
DEAD_BAL = float(0.15)

def handle_BAL(bal, user, pet, previous_bal):
    """Given a BAL, updates pet health and/or user status."""

    bal = bal.value
    if previous_bal != 0:
        previous_bal = previous_bal.value

    #if pet.sick_date is over 24 hours - multiply BAL by 1.5
    if pet.health == 'S':
        delta = timezone.now() - pet.sick_date
        if delta.days >= 1:
            bal = bal*1.5

    if bal == 0.0:
        return handle_zero_BAL(bal, pet)

    elif bal > 0 and bal < SICK_BAL:
        return handle_healthy_range_BAL(bal, user, pet, previous_bal)

    elif bal >= SICK_BAL and bal < DEAD_BAL:
        return handle_sick_range_BAL(bal, user, pet)

    elif bal >= DEAD_BAL:
        return handle_dead_range_BAL(bal, user, pet)


def handle_zero_BAL(bal, pet):

    if pet.health == 'S':
        pet.make_pet_healthy()
        return responses['zero_bal_pet_sick']

    return responses['zero_bal_pet_healthy']

def handle_healthy_range_BAL(bal, user, pet, previous_bal):

    if not user.on_watch:
        user.user_on_watch()
        return responses['healthy_range_bal_user_off_watch']

    elif user.on_watch:
        pk = user.pk
        if bal < previous_bal:
            user.user_off_watch()
            return responses['healthy_range_bal_user_on_watch_and_higher_previous']

        return responses['healthy_range_bal_user_on_watch_and_lower_previous']

def handle_sick_range_BAL(bal, user, pet):

    user.user_on_watch()

    if pet.health == 'H':
        pet.make_pet_sick()
        return responses['sick_range_bal_and_pet_healthy']

    return responses['sick_range_bal_and_pet_sick']

def handle_dead_range_BAL(bal, user, pet):

    user.user_off_watch()
    pet.kill_pet()
    return responses['dead_range_bal']

