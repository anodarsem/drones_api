from django.contrib import admin

from load.models import Medication


class MedicationAdmin(admin.ModelAdmin):
    exclude = ['drone']


admin.site.register(Medication, MedicationAdmin)

