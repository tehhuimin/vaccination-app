from django.db import models

# Time slots (enum values)
from enum import IntEnum
class TimeSlotChoices(IntEnum):
    AM10_AM11 = 1
    AM11_PM12 = 2
    PM12_PM01 = 3
    PM01_PM02 = 4
    PM02_PM03 = 5
    PM03_PM04 = 6
    PM04_PM05 = 7
    PM05_PM06 = 8

    @classmethod
    def choices(cls, list=None):
        names = {
            1 : "10:00 - 11:00",
            2 : "11:00 - 12:00",
            3 : "12:00 - 13:00",
            4 : "13:00 - 14:00", 
            5 : "14:00 - 15:00",
            6 : "15:00 - 16:00",
            7 : "16:00 - 17:00",
            8 : "17:00 - 18:00"
        }
        if list: 
            return [(key, names[key]) for key in list]
        
        return [(key.value, names[key.value]) for key in cls]

# User (Patient)
class User(models.Model):
    name = models.CharField(max_length=50)
    NRIC = models.CharField(max_length=9, primary_key=True)

    def __str__(self):
        return self.name

# Nurse 
class Nurse(models.Model):
    name = models.CharField(max_length=50)
    NRIC = models.CharField(max_length=9, primary_key=True)
    speed = models.IntegerField(default=10)

    def __str__(self):
        return self.name

# Vaccination Center 
class VaccinationCenter(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    max_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Nurse Availability
class NurseAvailability(models.Model): 
    id = models.AutoField(primary_key=True)
    NRIC = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.IntegerField(choices=TimeSlotChoices.choices(), default=TimeSlotChoices.AM10_AM11)
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['NRIC', 'date', 'time_slot', 'center'], name='nurse_availability')
        ]

# Booking
class Booking(models.Model): 
    id = models.AutoField(primary_key=True)
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.IntegerField(choices=TimeSlotChoices.choices(), default=TimeSlotChoices.AM10_AM11)
    NRIC = models.OneToOneField(User, on_delete=models.CASCADE)

