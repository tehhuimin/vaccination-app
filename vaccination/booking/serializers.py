from rest_framework import serializers
from .models import *


class VaccinationCenterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()

    class Meta: 
        model = VaccinationCenter
        fields = ('id', 'name')
