from django.db import models
from usuarios.models import Secretaria, Unidad, Oficinas
from proveedor.models import Proveedor



class Numero_registro(models.Model):
    numero= models.AutoField(primary_key=True) 



class Matarial_compras(models.Model):
    item = models.IntegerField() 
    descripcion= models.TextField(max_length=255, blank= False ,null= False)
    orden_compra=models.CharField(max_length=20, blank= False ,null= False)
    numero_formulario= models.IntegerField(default=0)
    unidad_manejo =models.CharField(max_length=20, blank= False ,null= False)
    fecha_creacion= models.DateTimeField(auto_now_add=True)
    fecha_compra= models.DateTimeField()
    secretaria= models.ForeignKey(Secretaria, blank=True , null=True,on_delete=models.RESTRICT,)
    secretaria_flag= models.BooleanField(default=False)
    unidad= models.ForeignKey(Unidad, blank=True , null=True,on_delete=models.RESTRICT,)
    unidad_flag= models.BooleanField(default=False)
    oficina= models.ForeignKey(Oficinas, blank=True , null=True,on_delete=models.RESTRICT,)
    oficina_flag= models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, blank=True , null=True,on_delete=models.RESTRICT,)
    flag = models.BooleanField(default=True)
    cantidad = models.IntegerField(default=0)
    costo_unitario =models.FloatField(default=0)
    costo_total =models.FloatField(blank=True, null=True, default=0)
    factura =models.CharField(max_length=255, blank= False ,null= False)
    estado_compra=models.CharField(default='PENDIENTE')
    numero_registro= models.ForeignKey(Numero_registro, blank=True , null=True,on_delete=models.RESTRICT,)



class Pedido_compras(models.Model):
    item = models.AutoField(primary_key=True) 
    material_compras = models.ForeignKey(Matarial_compras,null=True,on_delete=models.RESTRICT )
    cantidad_entrega =  models.IntegerField(default=0)
    estado_cardista = models.BooleanField( null= True, blank=True)
    fecha_cardista= models.DateTimeField(null= True, blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True)
