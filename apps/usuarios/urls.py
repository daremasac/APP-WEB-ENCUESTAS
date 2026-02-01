from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, exportar_excel_supervisor, dashboard_admin , editar_perfil, lista_usuarios,  gestionar_usuario, eliminar_usuario,detalle_usuario,listar_mi_equipo, crear_encuestador_supervisor, editar_encuestador_supervisor,ver_detalle_equipo,eliminar_encuestador_equipo

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'), # La raíz es el login
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard-general/', dashboard_admin, name='dashboard_admin'),
    path('perfil/', editar_perfil, name='editar_perfil'),

    # crud de usuarios para admin
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', gestionar_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', gestionar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/detalle/<int:pk>/', detalle_usuario, name='detalle_usuario'),

# --- ZONA SUPERVISOR (Mi Equipo) ---
    path('mi-equipo/', listar_mi_equipo, name='listar_mi_equipo'),
    path('mi-equipo/ver/<int:pk>/', ver_detalle_equipo, name='ver_detalle_equipo'),
    path('mi-equipo/nuevo/', crear_encuestador_supervisor, name='crear_encuestador'),
    path('mi-equipo/editar/<int:pk>/', editar_encuestador_supervisor, name='editar_encuestador'),
    path('mi-equipo/eliminar/<int:pk>/', eliminar_encuestador_equipo, name='eliminar_encuestador_equipo'),
     
     path('exportar_excel/', exportar_excel_supervisor, name='exportar_excel_supervisor'),


    # --- RECUPERACIÓN DE CONTRASEÑA ---
    # 1. El formulario donde pones tu correo
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(
             template_name="usuarios/password_reset.html",
             email_template_name="usuarios/password_reset_email.html" # <--- AGREGA ESTO
         ), 
         name='password_reset'),

    # 2. Mensaje de "Te hemos enviado un correo"
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="usuarios/password_reset_sent.html"), 
         name='password_reset_done'),

    # 3. El link que te llega al correo (para poner la nueva clave)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="usuarios/password_reset_form.html"), 
         name='password_reset_confirm'),

    # 4. Mensaje de éxito "Contraseña cambiada"
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/password_reset_done.html"), 
         name='password_reset_complete'),
]