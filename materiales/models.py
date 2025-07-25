from django.db import models

from proveedor.models import Proveedor


class Categoria(models.Model):
    codigo_clasificacion = models.CharField(max_length=100, unique=True , blank=False, null=False,verbose_name='Partida' ,error_messages={'unique':'El codigo de la categoria ya existe'})
    nombre= models.CharField(max_length=200, blank=False, unique=True, null=False, error_messages={'unique':'El nombre de la categoria ya existe'})
    es_habilitado=models.BooleanField(default=True)
    fecha_creacion= models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
  
        self.nombre = self.nombre.title()
       
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.nombre},{self.codigo_clasificacion}, {self.fecha_creacion}"




class Materiales(models.Model):
    nombre = models.CharField(max_length=255,blank=False, null=False,)
    codigo = models.CharField(max_length=255, blank=False, null=False)
    #marca = models.CharField(max_length=255, blank=False, null=False)
    stock = models.IntegerField(null=True, blank=True, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    #tamaño = models.CharField(max_length=255,blank=True, null=True)
    #color = models.CharField(max_length=100,blank=True, null=True)
    #unidad_medida = models.CharField(max_length=255,blank=True, null=True, verbose_name='Unidad de medida')
    unidad_manejo = models.CharField(max_length=255,blank=True, null=True, verbose_name='Unidad de manejo')
    #material = models.CharField(max_length=255,blank=True, null=True)
    
    #codigo_paquete = models.CharField(max_length=255, blank=True, null=True,  verbose_name='Codigo de paquete')
    categoria =models.ForeignKey(Categoria, models.CASCADE,blank=False, null=False )
    
    es_habilitado=models.BooleanField(default=True)
    gestion=  models.IntegerField(blank=True ,null=True) 
    cierre_gestion=  models.IntegerField(default=False) 
    

    def save(self, *args, **kwargs):
  
        self.nombre = self.nombre.title()
        #self.marca = self.marca.title() or None
        #self.color = self.color.title() or None
        #self.material = self.material.title() or None
        super().save(*args, **kwargs)

 
    def __str__(self) -> str:
        return f"""{self.nombre},{self.codigo},{self.fecha_creacion},
       {self.categoria}"""

   
class  Informacion_material(models.Model):
    #cantidad_paquete=models.IntegerField(blank=False, null=False, verbose_name='Cantidad por paquetes')
    cantidad_paquete_unidad = models.IntegerField(blank=False, null=False,verbose_name='unidad')
    #precio_paquete = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name='Precio por paquetes')
    precio_unidad=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name='Precio')
    total_precio= models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cantidad=models.IntegerField(null=True, blank=True)
    material = models.ForeignKey(Materiales, models.CASCADE, blank= False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    proveedor= models.ForeignKey(Proveedor, models.CASCADE,blank=False, null=False)
    factura = models.CharField(max_length=255,blank=False, null=False,)
    def calcular_total_cantidad(self):
       # self.cantidad= self.cantidad_paquete * self.cantidad_paquete_unidad
        self.save()
    def calcular_precio_total(self):
        self.total_precio= self.precio_paquete * self.precio_unidad
        self.save()

    def __str__(self):
        return f"{self.precio_unidad},{self.cantidad_paquete_unidad}"

