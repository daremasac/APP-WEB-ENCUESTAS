from django.contrib import admin

# view models 
from apps.ubigeo.models import Departamento, Provincia, Distrito
# Register your models here.
admin.site.register(Departamento)
admin.site.register(Provincia)
admin.site.register(Distrito)


