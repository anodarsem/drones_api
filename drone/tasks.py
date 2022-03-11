from datetime import datetime

from drone.models import Drone


def check_drone_battery_level():
    drones = Drone.objects.all()
    with open('drone_battery_level_logs.txt', 'w') as f:
        for d in drones:
            f.write("Time --- %s" % (datetime.now()))
            f.write("Drone %d battery level is %d" % (d.pk, d.battery_capacity))
