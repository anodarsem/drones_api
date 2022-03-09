from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Drone(models.Model):

    class ModelEnum(models.TextChoices):
        Lightweight = 'Lightweight'
        Middleweight = 'Middleweight'
        Cruiserweight = 'Cruiserweight'
        Heavyweight = 'Heavyweight'

    class StateEnum(models.TextChoices):
        IDLE = 'IDLE'
        LOADING = 'LOADING'
        LOADED = 'LOADED'
        DELIVERING = 'DELIVERING'
        DELIVERED = 'DELIVERED'
        RETURNING = 'RETURNING'

    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=25, choices=ModelEnum.choices)
    weight_limit = models.PositiveIntegerField(validators=[MaxValueValidator(500)])
    battery_capacity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    state = models.CharField(max_length=25, choices=StateEnum.choices, default=StateEnum.IDLE)

    def __str__(self):
        return self.serial_number
