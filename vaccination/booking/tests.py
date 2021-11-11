from django.test import TestCase, Client
from .models import * 
from django.urls import reverse
import json

nurses_list = [
  {
    "name": "Rhea Whitfield",
    "NRIC": 659075887, 
    "speed": 20
  },
  {
    "name": "Sweet Walker",
    "NRIC": 457726241, 
    "speed": 25
  },
  {
    "name": "Guadalupe Macias",
    "NRIC": 659356329
  },
  {
    "name": "Olson Kim",
    "NRIC": 696990834
  },
  {
    "name": "Amie Castaneda",
    "NRIC": 129207392, 
    "speed": 50
  },
  {
    "name": "Rita Farley",
    "NRIC": 481781064
  },
  {
    "name": "Earnestine Henderson",
    "NRIC": 971556002
  },
  {
    "name": "Macias Stanton",
    "NRIC": 844663759, 
    "speed": 24
  }
]

user_list = [
  {
    "name": "Sheena Barr",
    "NRIC": 273130972
  },
  {
    "name": "King Duke",
    "NRIC": 991673172
  },
  {
    "name": "Kay Huffman",
    "NRIC": 995246495
  },
  {
    "name": "Melisa Sharp",
    "NRIC": 335105107
  },
  {
    "name": "Karina Mejia",
    "NRIC": 742676741
  },
  {
    "name": "Witt Montoya",
    "NRIC": 820260963
  },
  {
    "name": "Jan Branch",
    "NRIC": 867133670
  },
  {
    "name": "Wilkins Schultz",
    "NRIC": 170419256
  }
]

center_list = [
    {
        "name": "Radin Mas Community Club", 
        "max_capacity": 50, 
    }, 
    {
        "name": "Buona Vista Community Club", 
        "max_capacity": 100, 
    }, 
    {
        "name": "Raffles City Convention Centre", 
        "max_capacity": 50, 
    }, 
    {
        "name": "Tanjong Pagar Community Club", 
        "max_capacity": 200, 
    }, 
    {
        "name": "Jalan Besar Community Club", 
        "max_capacity": 250, 
    }, 
    {
        "name": "Bishan Community Club", 
        "max_capacity": 150, 
    },
]

nurses_availability_list = [
    {
        "NRIC": 659075887, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.AM10_AM11, 
        "center": 1
    }, 
    {
        "NRIC": 659075887, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.AM11_PM12, 
        "center": 6
    }, 
    {
        "NRIC": 659075887, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "center": 2
    }, 
    {
        "NRIC": 659075887, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.PM02_PM03, 
        "center": 3
    }, 
    {
        "NRIC": 659075887, 
        "date": "2021-11-12", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "center": 2
    }, 
    {
        "NRIC": 971556002, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.AM10_AM11, 
        "center": 2
    }, 
    {
        "NRIC": 971556002, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.PM02_PM03, 
        "center": 2
    }, 
    {
        "NRIC": 971556002, 
        "date": "2021-11-12", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "center": 5
    }, 
    {
        "NRIC": 844663759, 
        "date": "2021-11-12", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "center": 1
    }, 
    {
        "NRIC": 844663759, 
        "date": "2021-11-13", 
        "time_slot": TimeSlotChoices.PM02_PM03, 
        "center": 1
    }, 
    {
        "NRIC": 844663759, 
        "date": "2021-11-13", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "center": 6
    }, 
    {
        "NRIC": 844663759, 
        "date": "2021-11-13", 
        "time_slot": TimeSlotChoices.AM10_AM11, 
        "center": 1
    },
    {
        "NRIC": 844663759, 
        "date": "2021-11-11", 
        "time_slot": TimeSlotChoices.AM10_AM11, 
        "center": 6
    },
]
booking_list = [
    {
        "center": 1, 
        "date" : "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "NRIC": "273130972"
    }, {
        "center": 2, 
        "date" : "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "NRIC": "991673172"
    }, 
    {
        "center": 2, 
        "date" : "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "NRIC": "995246495"
    }, 
    {
        "center": 2, 
        "date" : "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "NRIC": "742676741"
    }, 
    {
        "center": 2, 
        "date" : "2021-11-11", 
        "time_slot": TimeSlotChoices.PM01_PM02, 
        "NRIC": "820260963"
    }
]
    

class MyTest(TestCase):

    def setUp(self):
        """
            Setting up data for tests.
        """
        self.client = Client()
        # bulk create nurses 
        self.nurse_created = [Nurse.objects.create(**nurse) for nurse in nurses_list]
        self.user_created = [User.objects.create(**user) for user in user_list]
        self.center_created = [VaccinationCenter.objects.create(**center) for center in center_list]
        self.nurses_availability_created = [NurseAvailability.objects.create(NRIC=Nurse.objects.get(NRIC = availability.pop("NRIC")), center=VaccinationCenter.objects.get(id=availability.pop('center')), **availability) for availability in nurses_availability_list]
        self.all_bookings = [Booking.objects.create(center=VaccinationCenter.objects.get(id = booking.pop('center')), NRIC=User.objects.get(NRIC=booking.pop("NRIC")),  **booking) for booking in booking_list]



        
 



    




