from django.core.management.base import BaseCommand
from django.db import transaction
from apps.fichas.models import Dimension, Pregunta, Opcion

class Command(BaseCommand):
    help = 'Carga los datos maestros de la encuesta SIGERS05'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('--- 🚀 INICIANDO CARGA DE DATOS SIGERS ---'))

        # Estructura completa basada en SIGERS05
        estructura_encuesta = [
            {
                "nombre": "A. SOCIOECONÓMICAS",
                "descripcion": "Evaluación de ingresos y condiciones de vida.",
                "orden": 1,
                "preguntas": [
                    {
                        "orden": 1,
                        "enunciado": "Ingresos familiares mensuales totales:",
                        "opciones": [
                            ("Superior a S/. 3,391 o más de 3 salarios mínimos", 0),
                            ("Entre S/. 2,261 - S/. 3,390 o 2-3 salarios mínimos", 3),
                            ("Entre S/. 1,131 - S/. 2,260 o 1-2 salarios mínimos", 6),
                            ("Entre S/. 500 - S/. 1,130 o menos de 1 salario mínimo", 8),
                            ("Menor a S/. 500", 10),
                        ]
                    },
                    {
                        "orden": 2,
                        "enunciado": "Estabilidad laboral de la mamá:",
                        "opciones": [
                            ("Trabajo formal estable con beneficios", 0),
                            ("Trabajo formal temporal", 2),
                            ("Trabajo informal con cierta estabilidad", 4),
                            ("Trabajo informal sin estabilidad/subempleo", 6),
                            ("Sin empleo", 8),
                        ]
                    },
                    {
                        "orden": 3,
                        "enunciado": "Estabilidad laboral del papá:",
                        "opciones": [
                            ("Trabajo formal estable con beneficios", 0),
                            ("Trabajo formal temporal", 2),
                            ("Trabajo informal con cierta estabilidad", 4),
                            ("Trabajo informal sin estabilidad/subempleo", 6),
                            ("Sin empleo", 8),
                        ]
                    },
                    {
                        "orden": 4,
                        "enunciado": "Número de personas dependientes económicamente:",
                        "opciones": [
                            ("Sin dependientes", 0),
                            ("1-2 dependientes", 2),
                            ("3-4 dependientes", 4),
                            ("Más de 4 dependientes", 6),
                        ]
                    },
                    {
                        "orden": 5,
                        "enunciado": "Tipo de vivienda:",
                        "opciones": [
                            ("Propia, material noble/condiciones óptimas", 0),
                            ("Alquilada en zona segura, condiciones adecuadas", 2),
                            ("Prestada/cedida en condiciones aceptables", 3),
                            ("Alquilada en zona de riesgo", 5),
                            ("Precaria/invasión/alquiler de cuarto", 8),
                        ]
                    },
                    {
                        "orden": 6,
                        "enunciado": "Servicios básicos:",
                        "opciones": [
                            ("Acceso completo (agua, luz, desagüe, internet)", 0),
                            ("Agua, luz, desagüe", 1),
                            ("Solo agua y luz", 3),
                            ("Solo agua", 5),
                            ("Sin acceso a servicios básicos", 8),
                        ]
                    },
                    {
                        "orden": 7,
                        "enunciado": "Condiciones de hacinamiento:",
                        "opciones": [
                            ("Condiciones óptimas (menos de 2 personas por dormitorio)", 0),
                            ("Condiciones aceptables (2-3 personas por dormitorio)", 2),
                            ("Hacinamiento moderado (3-4 personas por dormitorio)", 4),
                            ("Hacinamiento severo (5-6 personas por dormitorio)", 6),
                            ("Hacinamiento crítico (más de 6 personas por dormitorio)", 8),
                        ]
                    },
                ]
            },
            {
                "nombre": "B. ESTRUCTURA Y DINÁMICA FAMILIAR",
                "descripcion": "Funcionalidad y relaciones.",
                "orden": 2,
                "preguntas": [
                    {
                        "orden": 8,
                        "enunciado": "8a. Estoy satisfecho con la ayuda que recibo de mi familia cuando algo me preocupa:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("Algunas veces", 3), ("Casi nunca", 4), ("Nunca", 5)
                        ]
                    },
                    {
                        "orden": 9,
                        "enunciado": "8b. Estoy satisfecho con la forma en que mi familia discute asuntos de interés común y comparte la solución del problema conmigo:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("Algunas veces", 3), ("Casi nunca", 4), ("Nunca", 5)
                        ]
                    },
                    {
                        "orden": 10,
                        "enunciado": "8c. Mi familia acepta mis deseos para promover nuevas actividades o hacer cambios en mi estilo de vida:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("Algunas veces", 3), ("Casi nunca", 4), ("Nunca", 5)
                        ]
                    },
                    {
                        "orden": 11,
                        "enunciado": "8d. Estoy satisfecho con la forma en que mi familia expresa afecto y responde a mis sentimientos de amor y tristeza:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("Algunas veces", 3), ("Casi nunca", 4), ("Nunca", 5)
                        ]
                    },
                    {
                        "orden": 12,
                        "enunciado": "8e. Estoy satisfecho con la cantidad de tiempo que mi familia y yo compartimos:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("Algunas veces", 3), ("Casi nunca", 4), ("Nunca", 5)
                        ]
                    },
                    {
                        "orden": 13,
                        "enunciado": "9. Estructura familiar:",
                        "opciones": [
                            ("Familia nuclear completa funcional", 0),
                            ("Familia monoparental funcional", 1),
                            ("Familia extendida funcional", 2),
                            ("Familia reconstituida funcional", 2),
                            ("Familia nuclear con disfuncionalidades", 4),
                            ("Familia monoparental con disfuncionalidades moderadas", 5),
                            ("Familia extendida con disfuncionalidades", 6),
                            ("Familia reconstituida con disfuncionalidades", 7),
                            ("Familia monoparental con múltiples carencias", 8),
                            ("Vive con otros familiares/terceros sin vínculos sólidos", 9),
                        ]
                    },
                    {
                        "orden": 14,
                        "enunciado": "10. Relaciones intrafamiliares:",
                        "opciones": [
                            ("Comunicación funcional y relaciones simétricas saludables", 0),
                            ("Comunicación adecuada con complementariedad flexible", 2),
                            ("Comunicación con dificultades puntuales", 4),
                            ("Patrones disfuncionales moderados", 5),
                            ("Comunicación predominantemente patológica", 6),
                            ("Comunicación gravemente alterada", 8),
                        ]
                    },
                    {
                        "orden": 15,
                        "enunciado": "11. Supervisión y cuidado parental:",
                        "opciones": [
                            ("Supervisión constante y adecuada para la edad", 0),
                            ("Supervisión ocasional pero efectiva", 2),
                            ("Supervisión insuficiente", 4),
                            ("Supervisión inadecuada o negligente", 6),
                            ("Ausencia total de supervisión", 8),
                        ]
                    },
                    {
                        "orden": 16,
                        "enunciado": "12. Antecedentes de violencia familiar:",
                        "opciones": [
                            ("Sin antecedentes de violencia familiar", 0),
                            ("Antecedentes de violencia superados con intervención exitosa", 1),
                            ("Violencia verbal/psicológica leve ocasional", 3),
                            ("Violencia psicológica moderada", 4),
                            ("Violencia psicológica grave sistemática", 6),
                            ("Violencia física menor esporádica", 5),
                            ("Violencia física menor pero recurrente", 7),
                            ("Violencia física grave sistemática", 10),
                            ("Violencia económica/patrimonial", 6),
                            ("Violencia sexual", 10),
                            ("Combinación de múltiples tipos de violencia", 10),
                        ]
                    },
                    {
                        "orden": 17,
                        "enunciado": "13. Distribución de roles y responsabilidades:",
                        "opciones": [
                            ("Distribución equilibrada de roles apropiados para la edad", 0),
                            ("Algunos desequilibrios menores en roles", 2),
                            ("Distribución desigual de responsabilidades", 4),
                            ("Roles invertidos, estudiante con responsabilidades de adulto", 6),
                        ]
                    },
                    {
                        "orden": 18,
                        "enunciado": "14. Problemas de salud mental en la familia:",
                        "opciones": [
                            ("No presenta problemas significativos de salud mental", 0),
                            ("Estrés/ansiedad leve manejable", 1),
                            ("Depresión/ansiedad que afecta funcionamiento", 3),
                            ("Problemas de conducta en algún miembro", 3),
                            ("Antecedentes de trastornos graves superados", 2),
                            ("Trastornos mentales severos actuales", 6),
                            ("Adicciones activas", 7),
                            ("Antecedentes recientes de intentos de suicidio", 8),
                            ("Múltiples casos de trastornos mentales graves", 9),
                            ("Situación crítica de salud mental", 10),
                        ]
                    },
                ]
            },
            {
                "nombre": "C. INDICADORES EDUCATIVOS",
                "descripcion": "Rendimiento y soporte educativo.",
                "orden": 3,
                "preguntas": [
                    {
                        "orden": 19,
                        "enunciado": "15. Nivel educativo de los padres/cuidadores (Promedio):",
                        "opciones": [
                            ("Educación superior completa", 0),
                            ("Educación superior incompleta/técnica", 1),
                            ("Secundaria completa", 2),
                            ("Secundaria incompleta", 3),
                            ("Primaria completa", 4),
                            ("Primaria incompleta", 5),
                            ("Analfabeta", 6),
                        ]
                    },
                    {
                        "orden": 20,
                        "enunciado": "16. Rendimiento académico del estudiante:",
                        "opciones": [
                            ("Logro destacado/satisfactorio", 0),
                            ("Buen rendimiento académico", 1),
                            ("Rendimiento promedio/en proceso", 3),
                            ("Rendimiento bajo/en inicio", 5),
                            ("Rendimiento muy bajo con riesgo de deserción/repitencia", 7),
                        ]
                    },
                    {
                        "orden": 21,
                        "enunciado": "17a. Asistencia escolar (EBR - Educación Básica Regular):",
                        "opciones": [
                            ("Asistencia regular (menos del 5% de faltas)", 0),
                            ("Ausencias ocasionales (5-10% de faltas)", 2),
                            ("Faltas frecuentes (11-15% de faltas)", 4),
                            ("Ausentismo preocupante (16-25% de faltas)", 6),
                            ("Ausentismo crónico/riesgo de deserción (más del 25%)", 8),
                        ]
                    },
                    {
                        "orden": 22,
                        "enunciado": "17b. Asistencia Estudiantes Universitarios:",
                        "opciones": [
                            ("Asistencia regular", 0),
                            ("Ausencias ocasionales", 2),
                            ("Faltas frecuentes", 4),
                            ("Riesgo académico por inasistencia", 6),
                            ("Patrón de deserción intermitente", 7),
                            ("Alto riesgo de deserción definitiva", 8),
                        ]
                    },
                    {
                        "orden": 23,
                        "enunciado": "18. Apoyo familiar en actividades educativas:",
                        "opciones": [
                            ("Apoyo constante y participación activa", 0),
                            ("Apoyo ocasional pero efectivo", 2),
                            ("Interés limitado o irregular", 3),
                            ("Apoyo insuficiente", 4),
                            ("Desinterés total/sin apoyo familiar", 6),
                        ]
                    },
                    {
                        "orden": 24,
                        "enunciado": "19a. Espacio físico en el hogar con adecuada iluminación, ventilación y mobiliario:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("A veces", 2), ("Casi nunca", 3), ("Nunca", 4)
                        ]
                    },
                    {
                        "orden": 25,
                        "enunciado": "19b. Material educativo adecuado y oportuno (libros, uniformes, útiles):",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("A veces", 2), ("Casi nunca", 3), ("Nunca", 4)
                        ]
                    },
                    {
                        "orden": 26,
                        "enunciado": "19c. Dispositivos electrónicos disponibles en el hogar (Laptop, tablet, celular):",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("A veces", 2), ("Casi nunca", 3), ("Nunca", 4)
                        ]
                    },
                    {
                        "orden": 27,
                        "enunciado": "19d. Conexión a internet suficiente en el hogar:",
                        "opciones": [
                            ("Siempre", 0), ("Casi siempre", 1), ("A veces", 2), ("Casi nunca", 3), ("Nunca", 4)
                        ]
                    },
                ]
            },
            {
                "nombre": "D. PSICOSOCIALES",
                "descripcion": "Estado emocional y conductual.",
                "orden": 4,
                "preguntas": [
                    {
                        "orden": 28,
                        "enunciado": "20. Estado emocional del estudiante:",
                        "opciones": [
                            ("Estable y adecuado para la edad", 0),
                            ("Tristeza/ansiedad ocasional normal", 2),
                            ("Cambios emocionales frecuentes", 4),
                            ("Síntomas depresivos/ansiosos persistentes", 6),
                            ("Indicadores de riesgo emocional severo", 8),
                        ]
                    },
                    {
                        "orden": 29,
                        "enunciado": "21. Comportamiento y habilidades sociales:",
                        "opciones": [
                            ("Conducta adecuada, relaciones interpersonales positivas", 0),
                            ("Participación social y relaciones formales", 2),
                            ("Problemas leves de conducta/socialización", 3),
                            ("Conductas disruptivas frecuentes/conflictos con pares", 5),
                            ("Aislamiento social severo/conductas agresivas", 7),
                        ]
                    },
                    {
                        "orden": 30,
                        "enunciado": "22. Participación en actividades escolares/universitarias:",
                        "opciones": [
                            ("Participación activa en actividades", 0),
                            ("Participación ocasional", 1),
                            ("Participación mínima", 3),
                            ("No participa/se aísla", 5),
                        ]
                    },
                    {
                        "orden": 31,
                        "enunciado": "23. Presencia de conductas de riesgo:",
                        "opciones": [
                            ("No presenta conductas de riesgo", 0),
                            ("Mentiras/faltas menores ocasionales", 2),
                            ("Conductas desafiantes frecuentes", 4),
                            ("Conductas autodestructivas/consumo de sustancias", 6),
                            ("Conductas delictivas/riesgo severo", 8),
                        ]
                    },
                    {
                        "orden": 32,
                        "enunciado": "24. Exposición a factores de riesgo del entorno:",
                        "opciones": [
                            ("Entorno seguro y protector", 0),
                            ("Exposición mínima a factores de riesgo", 2),
                            ("Exposición ocasional a situaciones de riesgo", 4),
                            ("Entorno de riesgo moderado", 6),
                            ("Alto riesgo (pandillaje, drogas, violencia)", 8),
                        ]
                    },
                ]
            },
            {
                "nombre": "E. ACCESO A SERVICIOS",
                "descripcion": "Salud y redes de apoyo.",
                "orden": 5,
                "preguntas": [
                    {
                        "orden": 33,
                        "enunciado": "25. Acceso a servicios de salud:",
                        "opciones": [
                            ("Acceso completo y oportuno", 0),
                            ("Acceso a servicios básicos", 2),
                            ("Acceso limitado, solo emergencias", 4),
                            ("Sin acceso a servicios de salud", 6),
                        ]
                    },
                    {
                        "orden": 34,
                        "enunciado": "26. Seguro de salud:",
                        "opciones": [
                            ("Sí (SIS, EsSalud, Fuerzas Armadas, EPS)", 0),
                            ("No", 4),
                        ]
                    },
                    {
                        "orden": 35,
                        "enunciado": "27. Estado de salud general de la familia:",
                        "opciones": [
                            ("Estado de salud general bueno", 0),
                            ("Problemas de salud menores o controlados", 2),
                            ("Algún miembro con problemas graves", 3),
                            ("Múltiples miembros con enfermedades crónicas graves", 5),
                        ]
                    },
                    {
                        "orden": 36,
                        "enunciado": "28. Participación en programas sociales:",
                        "opciones": [
                            ("Sin necesidad de programas sociales", 0),
                            ("Sin programas pero elegible", 2),
                            ("Beneficiario de 1-2 programas", 1),
                            ("Requiere programas pero no accede", 4),
                            ("Múltiples carencias no atendidas", 5),
                            ("Beneficiario de múltiples programas por necesidad extrema", 4),
                        ]
                    },
                    {
                        "orden": 37,
                        "enunciado": "29. Redes de apoyo social y comunitario:",
                        "opciones": [
                            ("Sólidas redes de apoyo", 0),
                            ("Algunas redes funcionales", 1),
                            ("Redes limitadas pero funcionales", 2),
                            ("Redes débiles o conflictivas", 4),
                            ("Ausencia de redes de apoyo", 6),
                        ]
                    },
                ]
            },
            {
                "nombre": "F. FACTORES PROTECTORES",
                "descripcion": "Puntos que restan riesgo.",
                "orden": 6,
                "preguntas": [
                    {
                        "orden": 38,
                        "enunciado": "30. Participación en organizaciones/actividades comunitarias:",
                        "opciones": [
                            ("Liderazgo activo", -3),
                            ("Participación activa", -2),
                            ("Participación ocasional/mínima", 0),
                            ("Sin participación", 1),
                        ]
                    },
                    {
                        "orden": 39,
                        "enunciado": "31. Prácticas religiosas/espirituales como soporte:",
                        "opciones": [
                            ("Prácticas regulares que brindan soporte", -2),
                            ("Prácticas ocasionales", -1),
                            ("Sin prácticas que brinden soporte", 0),
                        ]
                    },
                    {
                        "orden": 40,
                        "enunciado": "32. Proyectos de vida y resiliencia familiar:",
                        "opciones": [
                            ("Proyectos claros, alta resiliencia", -3),
                            ("Algunos proyectos, buena adaptación", -2),
                            ("Proyectos vagos o poco realizables", 0),
                            ("Sin proyectos claros, baja capacidad", 2),
                        ]
                    },
                    {
                        "orden": 41,
                        "enunciado": "33. Apoyo profesional actual:",
                        "opciones": [
                            ("Apoyo integral de múltiples profesionales", -3),
                            ("Apoyo profesional adecuado", -2),
                            ("Apoyo insuficiente", 1),
                            ("Sin apoyo profesional necesario", 3),
                        ]
                    },
                ]
            }
        ]

        try:
            with transaction.atomic():
                for dim_data in estructura_encuesta:
                    dimension, created = Dimension.objects.get_or_create(
                        nombre=dim_data["nombre"],
                        defaults={
                            "descripcion": dim_data["descripcion"],
                            "orden": dim_data["orden"]
                        }
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'Procesando: {dimension.nombre}'))

                    for preg_data in dim_data["preguntas"]:
                        pregunta, created_preg = Pregunta.objects.get_or_create(
                            enunciado=preg_data["enunciado"],
                            dimension=dimension,
                            defaults={"orden": preg_data["orden"]}
                        )
                        
                        if not created_preg:
                            pregunta.opciones.all().delete()
                            
                        for texto_opcion, puntaje in preg_data["opciones"]:
                            Opcion.objects.create(
                                pregunta=pregunta,
                                texto=texto_opcion,
                                puntaje=puntaje
                            )
            
            self.stdout.write(self.style.SUCCESS('✅ ¡CARGA EXITOSA! Base de datos poblada correctamente.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ ERROR: {e}'))