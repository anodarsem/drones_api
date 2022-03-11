from django.urls import path

from drone.views import DroneView, DroneLoadView, DroneLoadedMedicationView

app_name = 'drone'

urlpatterns = [
    path('register', DroneView.as_view({'post': 'register'}), name='register_drone'),
    path('available_drones', DroneView.as_view({'get': 'check_available_drones'}), name='check_available_drones'),
    path('battery_level/<int:pk>/', DroneView.as_view({'get': 'check_battery_level'}), name='check_battery_level'),
    path('drone/<int:drone_pk>/load/', DroneLoadView.as_view(), name='load_drone'),
    path('drone/<int:drone_pk>/loaded_medication/', DroneLoadedMedicationView.as_view(), name='loaded_medication'),

]
