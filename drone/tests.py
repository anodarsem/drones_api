from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from drone.models import Drone
from load.models import  Medication


class DroneTests(APITestCase):

    def test_register_drone_success(self):
        APIClient()

        data = {
            "loads": [],
            "serial_number": "01-TEST",
            "model": "Lightweight",
            "weight_limit": 450,
            "battery_capacity": 60,
            "state": "IDLE"
        }

        url = reverse('drone:register_drone')
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_register_drone_validations_fail(self):
        APIClient()

        data = {
            "loads": [],
            "serial_number": "01-TEST",
            "model": "other_model",
            "weight_limit": 600,
            "battery_capacity": 120.5,
            "state": "IDLE"
        }

        url = reverse('drone:register_drone')
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    def test_load_drone_over_weight(self):

        loads_pk = []

        drone = Drone.objects.create(serial_number='0001', weight_limit=450, battery_capacity=50, state="IDLE",
                                     model='Lightweight').pk
        load_1 = Medication.objects.create(name='Load_1', code='0001', weight=250).pk
        load_2 = Medication.objects.create(name='Load_2', code='0002', weight=300).pk

        loads_pk.append(load_1)
        loads_pk.append(load_2)

        data = {
            "loads": loads_pk
        }

        url = reverse('drone:load_drone',kwargs={'drone_pk':drone})
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

