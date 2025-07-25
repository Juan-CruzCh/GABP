from django.db import models
from  usuarios.models import Usuario
from materiales.models import Materiales
class Pedido(models.Model):
    unidad_manejo=models.CharField(max_length=20, blank= False ,null= False)
    numero_pedido=models.CharField(blank= True ,null= True)
    cantidad_pedida=models.IntegerField(blank=False, null=False, default=0)
    cantidad_entrega=models.IntegerField(blank= True ,null= True, default=0)
    descripcion = models.TextField(null=True)
    partida_presupuestada=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True, default=0)
    costo_unidad=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True, default=0)
    costo_total=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True, default=0)
    programa= models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    sub_programa=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    proyecto=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    act_u_obra=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    unidad_ejecucion=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    codigo_presupuesto=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    sub_cantidad_pedida=models.IntegerField(blank= True ,null= True, default=0)
    codigo_numero=models.DecimalField(max_digits=10, decimal_places=2,blank= True ,null= True)
    usuario=models.ForeignKey(Usuario , on_delete=models.RESTRICT , blank= False, null=False)
    material= models.ForeignKey(Materiales, on_delete=models.RESTRICT,  blank= False, null=False)
    precio_total=models.FloatField(blank= True ,null= True, default=0)

    aprobado_unidad = models.BooleanField( blank= True, null=True) #director administrativo
    aprobado_oficina = models.BooleanField( blank= True, null=True) 
    aprobado_presupuestos = models.BooleanField( blank= True, null=True) 
    aprobado_cardista = models.BooleanField( blank= True, null=True) 
    aprobado_almacen = models.BooleanField( blank= True, null=True) 

    aprobado_cardista_segunda=models.BooleanField( blank= True, null=True)

    aprobado_cardista_segunda_fecha =models.DateTimeField(blank=True, null=True)

    estado_pedido_almacen = models.CharField(blank=False, null=False, default='Pendiente')
    estado_de_pedido=models.CharField(blank=False, null=False, default='pendiente')
    fecha_pedido= models.DateTimeField(auto_now_add=True, blank=False, null=False)
    fecha_entrega_salida= models.DateTimeField(blank=True, null=True)
   
    
    def __str__(self) -> str:
        return f"Unidad de manejo: {self.unidad_manejo}, Cantidad pedido: {self.cantidad_pedida}, Cantidad entrega almacen: {self.cantidad_entrega}, Partida presupuestada: {self.partida_presupuestada},  Usuario: {self.usuario}, Producto: {self.material}, Fecha de pedido: {self.fecha_pedido}"
    def fecha_entrega_pedido(self):
        self.fecha_entrega_pedido= self.fecha_entrega_pedido(auto_now_add=True)
        self.save()

class Autorizacion_pedido(models.Model):#guarda la informacion de cada pedido autorizado, usuario, unidad
    estado_autorizacion= models.BooleanField(default=False)
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE, blank= False, null=False)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE, blank= False, null=False)
    fecha_de_autorizacion= models.DateTimeField(blank=True, null=True,auto_now_add=True)

    def __str__(self) -> str:
        return  f"{self.estado_autorizacion},{self.pedido},{self.usuario},{self.fecha_de_autorizacion}"

