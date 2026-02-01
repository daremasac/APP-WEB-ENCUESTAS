from django.urls import path
from . import views

urlpatterns = [
    path('api/provincias/', views.obtener_provincias, name='api_provincias'),
    path('api/distritos/', views.obtener_distritos, name='api_distritos'),
]