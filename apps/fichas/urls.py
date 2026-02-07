from django.urls import path
from .views import mis_encuestas,registrar_ficha,ver_ficha, exportar_excel,lista_instituciones,gestion_institucion,eliminar_institucion,lista_banco_preguntas,gestion_dimension,gestion_pregunta,eliminar_generico, listar_mis_fichas,editar_ficha

urlpatterns = [
    path('', mis_encuestas, name='fichas_root'),
    path('mis-encuestas/', mis_encuestas, name='mis_encuestas'),
    path('nueva-ficha-riesgo/', registrar_ficha, name='registrar_ficha'),
    path('ver-ficha/<int:ficha_id>/',ver_ficha, name='ver_ficha'),
    path('mis-fichas/', listar_mis_fichas, name='listar_fichas'),
    path('ficha/editar/<int:ficha_id>/', editar_ficha, name='editar_ficha'),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),

    # Instituciones
    path('config/instituciones/', lista_instituciones, name='lista_instituciones'),
    path('config/instituciones/crear/', gestion_institucion, name='crear_institucion'),
    path('config/instituciones/editar/<int:pk>/', gestion_institucion, name='editar_institucion'),
    path('config/instituciones/eliminar/<int:pk>/', eliminar_institucion, name='eliminar_institucion'),

    # Banco de Preguntas
    path('config/banco/', lista_banco_preguntas, name='lista_banco_preguntas'),
    
    path('config/dimension/crear/', gestion_dimension, name='crear_dimension'),
    path('config/dimension/editar/<int:pk>/', gestion_dimension, name='editar_dimension'),
    
    path('config/pregunta/crear/', gestion_pregunta, name='crear_pregunta'),
    path('config/pregunta/editar/<int:pk>/', gestion_pregunta, name='editar_pregunta'),
    
    # Eliminación Genérica para banco
    path('config/eliminar/<str:modelo>/<int:pk>/', eliminar_generico, name='eliminar_elemento'),
]


