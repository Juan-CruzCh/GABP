
from django.contrib.auth.models import AbstractBaseUser , UserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.db import models
from django.forms import ValidationError
from  persona.models import Persona
from django.utils.translation import gettext_lazy as _


    




class Secretaria(models.Model):
    secretaria = models.CharField(max_length=100, blank=False , null=False, unique=True)
    esHabilitado = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.secretaria}"
    

class Unidad(models.Model):
    nombre =models.CharField(max_length=100,blank=False, null=False, unique=True )
    secretaria=models.ForeignKey(Secretaria, on_delete=models.RESTRICT, blank= True, null=True)
    esHabilitado = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.nombre}"
    
class Oficinas(models.Model):
    nombre =models.CharField(max_length=100,blank=False, null=False, unique=True)
    unidad=models.ForeignKey(Unidad, on_delete=models.RESTRICT, blank= True, null=True)
    esHabilitado = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.nombre}"
    
@receiver(post_migrate)
def crear_entidades_por_defecto(sender, **kwargs):
    if sender.name == 'usuarios':
        secretaria, created = Secretaria.objects.get_or_create(secretaria='Secretaria departamental administrativa financiera')
        unidad, created = Unidad.objects.get_or_create(nombre='Financiera', secretaria=secretaria)
        Oficinas.objects.get_or_create(nombre='Almacenes', unidad=unidad)
        Oficinas.objects.get_or_create(nombre='Sistemas', unidad=unidad)
      



@receiver(post_migrate)
def crearUsuarioPorDefecto(sender, **kwargs):
    if sender.name == 'usuarios':
        if not Usuario.objects.exists():
            persona = Persona.objects.create(cedula_identidad='0000000', nombre='Test', apellidos='test')
            unidad = Unidad.objects.filter(nombre='Financiera').first()
            oficina = Oficinas.objects.filter(nombre='Sistemas').first()
            if unidad and oficina:  
                usuario = Usuario(
                    username='superadmin',
                    email='superadmin@gmail.com',
                    cargo='Encargado_oficina',
                    crear=False,
                    editar=False,
                    eliminar=False,
                    unidad=unidad,
                    oficina=oficina,
                    persona=persona,
                    rol='Super_administrador'
                )
                usuario.set_password('superadmin')  
                usuario.save()  


    
class Usuario(AbstractBaseUser, PermissionsMixin):
    def validate_image_file_extension(value):
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if not any(value.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError(_('Extension de archivo invalido'))
    CARGO_ROLE_CHOICES=[
        ('Presupuestos','Presupuestos'),
        ('Cardista','Kardixta'),
        ('Director_administrativo','Director Administrativo'),
        ('Encargado_oficina','Responsable de la oficina'),
        ('Usuario','Personal de la oficina'),
    ]
    ROLES_CHOICES=[
        ('Administrador','Administrador'),
        ('Super_administrador','Super administrador'),
        ('Auxiliar1','Auxiliar de Almacen'),
        ('Usuario','Usuario')
    ]
    username= models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name='Usuario')
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name='Contraseña')
    email=models.EmailField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    is_staff= models.CharField(default=True)#desactivar usuario

    cargo=models.CharField(blank=False, null=False, choices=CARGO_ROLE_CHOICES, default='Usuario', verbose_name='Encargado de unidad' ) 

    crear = models.BooleanField(default=False,verbose_name='Crear material')
    editar= models.BooleanField(default=False,verbose_name='editar material')
    eliminar=models.BooleanField(default=False,verbose_name='Eliminar material')
    rol=models.CharField(max_length=250, choices=ROLES_CHOICES, default='Personal')
    foto=models.ImageField(upload_to='upload/', blank=True , null=True,
         verbose_name='Imagen de perfil')
    unidad= models.ForeignKey(Unidad, on_delete=models.RESTRICT,blank=True, null=True)

    oficina= models.ForeignKey(Oficinas, on_delete=models.RESTRICT,blank=True, null=True)

    persona = models.ForeignKey(Persona, on_delete=models.RESTRICT)

    es_habilitado=models.BooleanField(default=True)
    es_activo=models.BooleanField(default=True)

    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['rol']
    def __str__(self) -> str:
        return f" Activo:{self.es_activo}"
    
    
