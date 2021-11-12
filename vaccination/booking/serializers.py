from rest_framework import serializers
from .models import *


class VaccinationCenterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()

    class Meta: 
        model = VaccinationCenter
        fields = ('id', 'name')

class BookingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='NRIC.name')
    NRIC = serializers.CharField(source='NRIC.NRIC')
    centerName = serializers.CharField(source='center.name')
    centerId = serializers.PrimaryKeyRelatedField(source='center.id', read_only=True)
    startTime = serializers.DateField(source='date')
    timeSlot = serializers.IntegerField(source='time_slot')

    class Meta: 
        model = Booking
        fields = ('id', 'name', 'NRIC', 'centerName', 'centerId', 'startTime', 'timeSlot')


class CreateBookingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    NRIC = serializers.CharField(required=True)
    centerId = serializers.IntegerField(required=True)
    date = serializers.DateField()
    time_slot = serializers.IntegerField()

    class Meta: 
        model = Booking
        fields = ( 'name', 'NRIC', 'centerId', 'date', 'time_slot')


class UpdateBookingSerializer(serializers.ModelSerializer):
    centerId = serializers.IntegerField()
    date = serializers.DateField()
    time_slot = serializers.IntegerField()

    class Meta: 
        model = Booking
        fields = ('centerId', 'date', 'time_slot')


