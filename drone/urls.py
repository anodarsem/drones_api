from django.urls import path

from drone.views import DroneView

urlpatterns = [
    path('register', DroneView.as_view({'post': 'register'}), name='register_drone'),
    path('available_drones', DroneView.as_view({'get': 'check_available_drones'}), name='check_available_drones'),
    path('battery_level/<int:pk>/', DroneView.as_view({'get': 'check_battery_level'}), name='check_battery_level'),

]
