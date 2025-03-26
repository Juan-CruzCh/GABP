from django.urls import path
from .views import imprecion_solicitud_costo,listar_pedido_codigo_cardista_almacen,listar_pedidos_cardista_costo_almacen,index,asignar_costo,asignar_partida_presupuestada,listar_pedido_codigo_cardista,listar_pedidos_cardista_costo,reporte_pedido_salida,rechazar_pedido_almacen, rechazar_pedido_presupuestos,rechazar_pedido_oficina,cancelar_todos_los_pedidos,autorizar_pedidos_cardista,listar_pedidos_por_codigo_presupuesto,listar_pedidos_presupuestos,autorizar_pedidos_presupuestos,rechazar_pedido_cardista,listar_pedidos_por_codigo_cardista,listar_pedidos_cardista,listar_pedidos_por_codigo_oficina,eliminar_mi_pedido_carrito,sub_pedido_almacen,reporte_pedidos,autorizar_pedidos_oficina,listar_pedidos_por_codigo,listar_pedidos_oficina ,sub_pedido,lista_pedido_por_id,cambiar_estado_pedido,listar_info_material,realizar_entrega,imprecion_solicitud,autorizar_pedidos_almacen,listando_pedido_almacen,generate_pdf,buscador,mostrar_informacion_pedidio_aprobaciones, realizar_pedido, listar_pedidos_usuarios_almacen, mis_pedidos,todos_mis_pedidos, listar_pedidos_unidad, autorizar_pedidos, rechazar_pedido_unidad, eliminar_mi_pedido

urlpatterns = [
   path('index',index , name='index' ),
   path('buscar',buscador , name='buscar' ),
   path('realizar_pedido',realizar_pedido , name='realizar_pedido' ),
   path('listando_pedidos',listar_pedidos_usuarios_almacen , name='listando_pedidos' ),
   path('informacion_pedido/<str:numero>',listando_pedido_almacen , name='informacion_pedido' ),
   path('mis_pedidos',mis_pedidos , name='mis_pedidos' ),
   path('todos_mis_pedidos',todos_mis_pedidos, name='todos_mis_pedidos' ),
   path('listar_pedidos_unidad',listar_pedidos_unidad, name='listar_pedidos_unidad' ),
      path('listar_pedidos_cardista',listar_pedidos_cardista, name='listar_pedidos_cardista' ),
       path('listar_pedidos_presupuestos',listar_pedidos_presupuestos, name='listar_pedidos_presupuestos' ),

       path('cancelar_todos_los_pedidos',cancelar_todos_los_pedidos, name='cancelar_todos_los_pedidos' ),



   path('listar_pedidos_oficina',listar_pedidos_oficina, name='listar_pedidos_oficina' ),

    path('autorizar_pedidos_cardista/<int:id_pedido>',autorizar_pedidos_cardista, name='autorizar_pedidos_cardista' ),
path('autorizar_pedidos_presupuestos/<int:id_pedido>',autorizar_pedidos_presupuestos, name='autorizar_pedidos_presupuestos' ),
   path('autorizar_pedido/<int:id_pedido>',autorizar_pedidos, name='autorizar_pedido' ),
    path('autorizar_pedido_oficina/<int:id_pedido>',autorizar_pedidos_oficina, name='autorizar_pedido_oficina' ),
   path('autorizar_pedido_almacen/<int:id_pedido>',autorizar_pedidos_almacen, name='autorizar_pedido_almacen' ),
   path('rechazar_pedido_unidad/<int:id_pedido>',rechazar_pedido_unidad, name='rechazar_pedido_unidad' ),
         path('rechazar_pedido_oficina/<int:id_pedido>',rechazar_pedido_oficina, name='rechazar_pedido_oficina' ),
    
      path('rechazar_pedido_cardista/<int:id_pedido>',rechazar_pedido_cardista, name='rechazar_pedido_cardista' ),
         path('rechazar_pedido_almacen/<int:id_pedido>',rechazar_pedido_almacen, name='rechazar_pedido_almacen' ),
            path('rechazar_pedido_presupuestos/<int:id_pedido>',rechazar_pedido_presupuestos, name='rechazar_pedido_presupuestos' ),
   path('eliminar_mi_pedido/<int:id_pedido>',eliminar_mi_pedido, name='eliminar_mi_pedido'),
      path('eliminar/mi_pedido/carrito/<int:id_pedido>',eliminar_mi_pedido_carrito, name='eliminar_mi_pedido_carrito'),
   path('informacion/pedido/<int:id_pedido>' , mostrar_informacion_pedidio_aprobaciones , name="info_aprobaciones" ),
   path('imprimir/<str:numero>',imprecion_solicitud, name='imprimir' ),
      path('imprimir/costo/<str:numero>',imprecion_solicitud_costo, name='imprimir_costo' ),

   path('generar/pdf/<str:numero>',generate_pdf, name='pdf' ),
   path('informacion_pedido/lista_pedido_por_id/<int:id_pedido>',lista_pedido_por_id, name='lista_pedido_por_id' ),
   path('realizar_entrega',realizar_entrega, name='realizar_entrega' ),
   path('listar_info_material/<int:id_material>',listar_info_material, name='listar_info_material' ),
   path('cambiar_estado_pedido',cambiar_estado_pedido, name='cambiar_estado_pedido' ),
   path('sub_pedido',sub_pedido, name='sub_pedido' ),
   path('sub_pedido_almacen/',sub_pedido_almacen, name='sub_pedido_almacen' ),
   
   path('pedidos/numero/<str:numero>',listar_pedidos_por_codigo, name='pedido_numero' ),
               path('pedidos/oficina/numero/<str:numero>',listar_pedidos_por_codigo_oficina, name='pedido_numero_oficina' ),
               path('pedidos/cardista/numero/<str:numero>',listar_pedidos_por_codigo_cardista, name='pedido_numero_cardista' ),
                path('pedidos/presupuestos/numero/<str:numero>',listar_pedidos_por_codigo_presupuesto, name='listar_pedidos_por_codigo_presupuesto' ),
          path('pedidos/reporte',reporte_pedidos, name='reporte_pedidos' ),
                          path('pedido/salida',reporte_pedido_salida , name='reporte_pedido_salida' ),
    path('pedido/costo/cardista',listar_pedidos_cardista_costo , name='listar_pedidos_cardista_costo' ),
          path('pedido/costo/cardista/almacen',listar_pedidos_cardista_costo_almacen , name='listar_pedidos_cardista_costo_almacen' ),
      
   path('pedido/costo/cardista/codigo/<str:codigo>',listar_pedido_codigo_cardista , name='listar_pedidos_cardista_costo_codigo' ),
   path('pedido/costo/cardista/codigo/almacen/<str:codigo>',listar_pedido_codigo_cardista_almacen , name='listar_pedido_codigo_cardita_almacen' ),
      
       path('pedido/costo/asignar',asignar_costo , name='asignar_costo' ),
        
    path('pedido/partida/presupuestada',asignar_partida_presupuestada , name='partida_presupuestada' ),
        
                      
   
]