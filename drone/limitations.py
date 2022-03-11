from django.db.models import Sum

from drone.models import Drone


def get_load_total_weight(medication_list):
    total_weight = medication_list.aggregate(Sum('weight'))
    return total_weight['weight__sum'] if total_weight['weight__sum'] is not None else 0


def can_be_loaded_weight(drone, medication_list):
    drone_weight_limit = Drone.objects.get(pk=drone.pk).weight_limit
    drone_loaded_weight = get_load_total_weight(medication_list)

    if drone_loaded_weight <= drone_weight_limit:
        return True
    return False


def can_be_loaded_battery_level(drone):
    if drone.battery_capacity >= 25:
        return True
    return False






