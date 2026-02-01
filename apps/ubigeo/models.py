from django.db import models

class Departamento(models.Model):
    id = models.CharField('Código', max_length=2, primary_key=True) # Ej: 01
    nombre = models.CharField('Departamento', max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    id = models.CharField('Código', max_length=4, primary_key=True) # Ej: 0101
    nombre = models.CharField('Provincia', max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')

    def __str__(self):
        return f"{self.nombre} ({self.departamento})"

class Distrito(models.Model):
    id = models.CharField('Código', max_length=6, primary_key=True) # Ej: 010101
    nombre = models.CharField('Distrito', max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')
    
    # Opcional: Datos extra de tu CSV
    region_natural = models.CharField('Región Natural', max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.provincia.nombre}"