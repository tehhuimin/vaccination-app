from .models import * 
from django.db.models import Sum
def calculate_center_capacity(center_id, selected_date, time_slot) -> int: 
    return min(
        NurseAvailability.objects.filter(
                date=selected_date, 
                center__id=center_id, 
                time_slot=time_slot
            ).values('NRIC__speed').aggregate(Sum('NRIC__speed')).get('NRIC__speed__sum') or 0, 
        VaccinationCenter.objects.get(id=center_id).max_capacity
        )

def check_centers_total_booking(center_id, selected_date, time_slot) -> int:
    return Booking.objects.filter(
        date=selected_date, 
        center__id=center_id, 
        time_slot=time_slot
    ).count()

def check_center_available_for_booking(center_id, selected_date, time_slot)->bool:
    return check_centers_total_booking(center_id, selected_date, time_slot) < calculate_center_capacity(center_id, selected_date, time_slot)

def get_list_of_slots_available(center_id, selected_date) -> list:
    list = []
    for choice, value in TimeSlotChoices.choices(): 
        if check_center_available_for_booking(center_id, selected_date, choice): 
            list.append(choice)
    return list
