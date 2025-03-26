from django.urls import path, include 
from .views  import login_sistema,editar_oficina,manual_usuario, ayuda_tecnica,editar_secretaria, editar_unidad, listar_secretaria,backup_database,soft_delete_secretaria, soft_delete_oficina, soft_delete_undiad,listar_unidad, listar_oficina,organigrama,mi_perfil,cambiar_contrasena,enviar_correos,buscar_cuenta,crear_oficinas,Crear_unidad_secretaria,logout_view,crear_unidad_listar,oficinas_listar, creando_usuario, listando_usuarios, crear_secretaria_listar,soft_delete, activar_cuenta, desactivar_cuenta, actulizar_cuenta_usuario
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [

    path("", login_sistema, name="login"),
    path("creando_usuarios", creando_usuario, name="creando_usuarios"),
    path('listando_usuarios',listando_usuarios,name='listando_usuarios' ),
    path('crear_secretaria_listar',crear_secretaria_listar,name='crear_secretaria_listar' ),
    path('eliminar/<int:id>', soft_delete, name='eliminar_cuenta') ,
    path('activar_cuenta/<int:id>', activar_cuenta, name='activar_cuenta') ,
    path('desactivar_cuenta/<int:id>', desactivar_cuenta, name='desactivar_cuenta') ,
    path('actulizar_cuenta_usuario/<int:id_usuario>/<int:id_persona>', actulizar_cuenta_usuario, name='actulizar_cuenta_usuario') ,
    path("logout", logout_view, name='logout'),
    path("unidad",crear_unidad_listar , name='unidad' ),
        path("listar/unidad",listar_unidad , name='listar_unidad' ),
              path("listar/oficina",listar_oficina , name='listar_oficina' ),
                      path("listar/secretaria",listar_secretaria , name='listar_secretaria' ),

                        path("delte/unidad/<int:id>",soft_delete_undiad , name='delete_unidad' ),
              path("delete/oficina/<int:id>",soft_delete_oficina , name='delete_oficina' ),
                      path("delete/secretaria/<int:id>",soft_delete_secretaria , name='delete_secretaria' ),

 
    path('oficinas/<int:id_unidad>',oficinas_listar, name='oficinas'),

    path('crear_oficinas',crear_oficinas, name='crear_oficinas'),
    path('Crear_unidad_secretaria', Crear_unidad_secretaria, name='Crear_unidad_secretaria'),
    path('mi_perfil/<int:id_usuario>', mi_perfil, name='mi_perfil'),
    path('buscar/cuenta/<str:email>', buscar_cuenta, name='buscar_cuenta'),
       path('enviar_correos/<int:id_usuario>', enviar_correos, name='enviar_correos'),
              path('organigrama', organigrama, name='organigrama'),
              path('cambiar_contrasena/<int:id_usuario>', cambiar_contrasena, name='cambiar_contrasena'),
             path('backup/create',backup_database, name='backup_database'),

     path('editar/oficina/<int:id>',editar_oficina, name='editar_oficina'),
        path('editar/secretaria/<int:id>',editar_secretaria, name='editar_secretaria'),
           path('editar/unidad/<int:id>',editar_unidad, name='editar_unidad'),
                 path('ayuda/tecnica',ayuda_tecnica, name='ayuda_tecnica'),
                       path('manual/usuario',manual_usuario, name='manual_usuario')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)