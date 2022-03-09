from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from drone.models import Drone
from drone.serializers import DroneSerializer


class DroneView(viewsets.ModelViewSet):
    

    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_available_drones(self, request):
        available_drones = Drone.objects.filter(Q(state="IDLE", battery_capacity__gt=25)|Q(state="LOADING", battery_capacity__gt=25))
        serializer = DroneSerializer(available_drones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def check_battery_level(self, request, pk=None):
        try:
            battery_level = Drone.objects.get(pk=pk)
            serializer = DroneSerializer(battery_level, many=False)
            return Response(serializer.data['battery_capacity'], status=status.HTTP_200_OK)
        except:
            return Response('Drone pk does not exist', status=status.HTTP_404_NOT_FOUND)

        

