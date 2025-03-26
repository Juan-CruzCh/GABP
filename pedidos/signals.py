# pedidos/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils.enviar_notificacion import enviar_notificacion_pedido


def enviar_notificacion_nuevo_pedido(sender, instance, created, **kwargs):
    if created:
        enviar_notificacion_pedido(instance)
