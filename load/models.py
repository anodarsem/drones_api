from email.mime import image
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from drone.models import Drone


def upload_to(instance, filename):
    return 'loads/medications/{filename}'.format(filename=filename)


class Load(models.Model):

    weight = models.PositiveIntegerField(default=0)
    drone = models.ForeignKey(Drone, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Medication(Load):

    name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z0-9_-]*$', message='Field only allows letters, numbers, -, _')])
    code = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Z0-9_]*$', message='Field only allows uppercase letters, numbers, _')])
    image = models.ImageField(_("Image"), upload_to=upload_to, default='loads/medications/default.jpg')

    def __str__(self):
        return self.name
