from django.db import models

class Logs_sistema(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)  
    user =  models.CharField(max_length=255)
    accion = models.CharField(max_length=255) 
    detalle = models.TextField()
    modelo = models.CharField(max_length=255) 
    def __str__(self):
        return f"{self.fecha} - {self.user} - {self.detalle} - {self.accion}"