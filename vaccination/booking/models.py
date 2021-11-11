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
    def choices(cls):
        return [(key.value, key.name) for key in cls]

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
    name = models.CharField(max_length=50)
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

