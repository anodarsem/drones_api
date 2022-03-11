from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from load.models import Medication
from .models import Drone


class DroneSerializer(serializers.ModelSerializer):
    loads = PrimaryKeyRelatedField(many=True, read_only=False, queryset=Medication.objects.filter(drone__isnull=True))

    class Meta:
        model = Drone
        fields = '__all__'




