from django.db import models

from  persona.models import Persona

class Proveedor(models.Model):
    empresa= models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=255)
    descripcion= models.TextField( null=True)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100, default='POTOSI')
    direccion = models.CharField(max_length=100)
    fecha_creacion= models.DateTimeField(auto_now_add=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    es_habilitado=models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.empresa}, {self.nit}, {self.telefono}, {self.correo}, {self.pais}, {self.direccion}, {self.fecha_creacion}"
    