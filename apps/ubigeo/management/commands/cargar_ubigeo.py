import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.ubigeo.models import Departamento, Provincia, Distrito

class Command(BaseCommand):
    help = 'Carga la data de Ubigeos desde el CSV interno de la app'

    def handle(self, *args, **kwargs):
        # 1. CALCULAR RUTA
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_app_ubigeo = os.path.dirname(os.path.dirname(ruta_script))
        archivo_csv = os.path.join(ruta_app_ubigeo, 'data', 'UBIGEOS_2022_1891_distritos.csv')
        
        if not os.path.exists(archivo_csv):
            self.stdout.write(self.style.ERROR(f'❌ No se encontró el archivo en: {archivo_csv}'))
            return

        print(f"--- 🚀 LEYENDO DESDE: {archivo_csv} ---")
        
        deps_creados = 0
        provs_creadas = 0
        dists_creados = 0

        try:
            # Usamos 'latin-1' para soportar tildes y Ñ
            with open(archivo_csv, mode='r', encoding='latin-1') as f:
                # Si tu CSV usa comas en lugar de punto y coma, cambia delimiter=','
                reader = csv.DictReader(f, delimiter=';') 
                
                with transaction.atomic():
                    # Usamos enumerate para contar filas de forma segura (i)
                    for i, row in enumerate(reader):
                        
                        # 1. LIMPIEZA Y VALIDACIÓN
                        # Usamos .get() para evitar error si la columna no existe o está vacía
                        ubigeo = row.get('IDDIST', '').strip()
                        
                        # ¡AQUÍ ESTÁ LA SOLUCIÓN!: Si el ubigeo está vacío, saltamos la fila
                        if not ubigeo:
                            continue
                            
                        # Desglose del código
                        cod_dep = ubigeo[0:2]
                        cod_prov = ubigeo[0:4]
                        cod_dist = ubigeo
                        
                        nombre_dep = row.get('NOMBDEP', '').strip()
                        nombre_prov = row.get('NOMBPROV', '').strip()
                        nombre_dist = row.get('NOMBDIST', '').strip()
                        region = row.get('REGION NATURAL', '').strip()

                        # 2. DEPARTAMENTO
                        dep_obj, created_dep = Departamento.objects.get_or_create(
                            id=cod_dep,
                            defaults={'nombre': nombre_dep}
                        )
                        if created_dep: deps_creados += 1

                        # 3. PROVINCIA
                        prov_obj, created_prov = Provincia.objects.get_or_create(
                            id=cod_prov,
                            defaults={
                                'nombre': nombre_prov,
                                'departamento': dep_obj
                            }
                        )
                        if created_prov: provs_creadas += 1

                        # 4. DISTRITO
                        dist_obj, created_dist = Distrito.objects.get_or_create(
                            id=cod_dist,
                            defaults={
                                'nombre': nombre_dist,
                                'provincia': prov_obj,
                                'region_natural': region
                            }
                        )
                        if created_dist: dists_creados += 1

                        # Reporte de progreso cada 500 filas (Usando contador i, no el valor del ubigeo)
                        if i % 500 == 0:
                            self.stdout.write(f"Procesando fila {i}... {nombre_dist}")

            self.stdout.write(self.style.SUCCESS(f"""
            ✅ ¡CARGA EXITOSA!
            -----------------------
            Departamentos: {deps_creados}
            Provincias:    {provs_creadas}
            Distritos:     {dists_creados}
            """))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))