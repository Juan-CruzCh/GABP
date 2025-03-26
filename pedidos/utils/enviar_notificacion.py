# pedidos/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# pedidos/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from usuarios.models import Usuario

def enviar_notificacion_pedido(request, pedido):
    channel_layer = get_channel_layer()
    
    if request.user.cargo == 'Usuario':

        jefe_oficina = Usuario.objects.filter(oficina=request.user.oficina, cargo='Encargado_oficina')
        
        for u in jefe_oficina:
          
            group_name = f'notificaciones_{u.id}'  
            
            async_to_sync(channel_layer.group_send)(
                group_name,  
                {
                    'type': 'enviar_pedido',
                    'pedido': {
                        'nombre': f"{pedido.usuario.persona.nombre} {pedido.usuario.persona.apellidos}",
                        'codigo': pedido.numero_pedido,
                        'cantidad_pedida': pedido.cantidad_pedida,
                    }
                }
            )
    elif request.user.cargo == 'Encargado_oficina':
    
        jefe_oficina = Usuario.objects.filter(cargo='Director_administrativo')
        
        for u in jefe_oficina:
          
            group_name = f'notificaciones_{u.id}'  
            
            async_to_sync(channel_layer.group_send)(
                group_name,  
                {
                    'type': 'enviar_pedido',
                    'pedido': {
                        'nombre': f"{pedido.usuario.persona.nombre} {pedido.usuario.persona.apellidos}",
                        'codigo': pedido.numero_pedido,
                        'cantidad_pedida': pedido.cantidad_pedida,
                    }
                }
            )
    elif request.user.cargo == 'Director_administrativo':

        jefe_oficina = Usuario.objects.filter(cargo='Cardista')
        
        for u in jefe_oficina:
          
            group_name = f'notificaciones_{u.id}'  
            
            async_to_sync(channel_layer.group_send)(
                group_name,  
                {
                    'type': 'enviar_pedido',
                    'pedido': {
                        'nombre': f"{pedido.usuario.persona.nombre} {pedido.usuario.persona.apellidos}",
                        'codigo': pedido.numero_pedido,
                        'cantidad_pedida': pedido.cantidad_pedida,
                    }
                }
            )
    elif request.user.cargo == 'Cardista':

        jefe_oficina = Usuario.objects.filter(cargo='Presupuestos')
        
        for u in jefe_oficina:
          
            group_name = f'notificaciones_{u.id}'  
            
            async_to_sync(channel_layer.group_send)(
                group_name,  
                {
                    'type': 'enviar_pedido',
                    'pedido': {
                        'nombre': f"{pedido.usuario.persona.nombre} {pedido.usuario.persona.apellidos}",
                        'codigo': pedido.numero_pedido,
                        'cantidad_pedida': pedido.cantidad_pedida,
                    }
                }
            )
    elif request.user.cargo == 'Presupuestos':

        jefe_oficina = Usuario.objects.filter(oficina__nombre='Almacenes')
        
        for u in jefe_oficina:
          
            group_name = f'notificaciones_{u.id}'  
            
            async_to_sync(channel_layer.group_send)(
                group_name,  
                {
                    'type': 'enviar_pedido',
                    'pedido': {
                        'nombre': f"{pedido.usuario.persona.nombre} {pedido.usuario.persona.apellidos}",
                        'codigo': pedido.numero_pedido,
                        'cantidad_pedida': pedido.cantidad_pedida,
                    }
                }
            )
