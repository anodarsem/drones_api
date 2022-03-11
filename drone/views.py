from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from drone.limitations import can_be_loaded_weight, can_be_loaded_battery_level
from drone.models import Drone
from drone.serializers import DroneSerializer
from load.models import Medication
from load.serializers import MedicationSerializer


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
        available_drones = Drone.objects.filter(state="IDLE", battery_capacity__gt=25)
        serializer = DroneSerializer(available_drones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def check_battery_level(self, request, pk=None):
        try:
            battery_level = Drone.objects.get(pk=pk)
            serializer = DroneSerializer(battery_level, many=False)
            return Response({'battery_capacity':serializer.data['battery_capacity']}, status=status.HTTP_200_OK)
        except Drone.DoesNotExist:
            return Response('Drone pk does not exist', status=status.HTTP_404_NOT_FOUND)


class DroneLoadedMedicationView(APIView):

    def get(self, request, drone_pk=None):
        try:
            drone = Drone.objects.get(pk=drone_pk).loads.all()

            serializer = MedicationSerializer(drone, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Drone.DoesNotExist:
            return Response('Drone pk does not exist', status=status.HTTP_404_NOT_FOUND)


class DroneLoadView(APIView):

    def post(self, request, drone_pk=None):
        try:
            drone = Drone.objects.get(pk=drone_pk)
            medication = Medication.objects.filter(pk__in=request.data['loads'])
            if drone.state in ["LOADING", "IDLE"]:
                if can_be_loaded_weight(drone, medication):
                    if can_be_loaded_battery_level(drone):
                        drone.state = "LOADING"
                        drone.save()
                        medication.update(drone=drone)
                        drone.state = "LOADED"
                        drone.save()
                        return Response(status=status.HTTP_202_ACCEPTED)

                    else:
                        return Response('Drone battery level below 25%', status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response('Load weight is upper than drone weight limit',
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response('Drone is not in IDLE or LOADING status', status=status.HTTP_406_NOT_ACCEPTABLE)

        except Drone.DoesNotExist:
            return Response('Drone pk does not exist', status=status.HTTP_404_NOT_FOUND)





        

