from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Provincia, Distrito

def obtener_provincias(request):
    # Recibimos el ID del departamento desde la petición AJAX
    dep_id = request.GET.get('dep_id')
    provincias = Provincia.objects.filter(departamento_id=dep_id).order_by('nombre')
    # Convertimos a lista de diccionarios para JSON
    data = [{'id': p.id, 'nombre': p.nombre} for p in provincias]
    return JsonResponse(data, safe=False)

def obtener_distritos(request):
    prov_id = request.GET.get('prov_id')
    distritos = Distrito.objects.filter(provincia_id=prov_id).order_by('nombre')
    data = [{'id': d.id, 'nombre': d.nombre} for d in distritos]
    return JsonResponse(data, safe=False)