from django.db import models

# Create your models here.
class Pedido_compras(models.Model):
    cantidad=models.IntegerField(default=0)
    catidad_entrefa=models.IntegerField(default=0)
    costo=models.FloatField(default=0)
    aprobado_almacen=models.BooleanField()
    estado_pedido=models.CharField(default='PENDIENTE')
    estado_cardista=models.BooleanField(default=False)
    fecha_creacion= models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=True)
