from django.apps import AppConfig


class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'



class PedidosConfig(AppConfig):
    name = 'pedidos'

    def ready(self):
        import pedidos.signals
