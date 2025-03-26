import os
import datetime
import subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.http import JsonResponse, FileResponse
from django.conf import settings
from pathlib import Path
from django.shortcuts import render
from base64 import b64encode
from cryptography.hazmat.primitives import padding
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.urls import reverse

from logs.views import crear_log_sistema
from .forms import Usuario_formulario, Usuario_formulario_actulizar
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import os
from dotenv import load_dotenv

from .models import Usuario, Secretaria, Oficinas, Unidad

from django.http import FileResponse, JsonResponse

from persona.forms import Formulario_persona 

from utils.paginador import paginador_general
from persona.models import Persona 


load_dotenv()
def login_sistema(request):
    if(request.method=='POST'):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.es_activo and user.es_habilitado:
                login(request, user)
                if user.username =='superadmin':
                    detalle = f'El usuario {username} ha ingresado al sistema exitosamente.'
                    crear_log_sistema(username, 'Ingreso exitoso', detalle, 'Usuario') 
                    return  redirect('administracion')
                detalle = f'El usuario {username} ha ingresado al sistema exitosamente.'
                crear_log_sistema(username, 'Ingreso exitoso', detalle, 'Usuario')
                return redirect('index')
        else:
            detalle = f'El usuario {username} intentó ingresar al sistema, pero la autenticación falló.'
            crear_log_sistema(username, 'Intento de ingreso fallido', detalle, 'Usuario')
            return render(request, 'usuarios/login.html', {'error_message': 'Credenciales inválidas'})
    else:
        return render(request, 'usuarios/login.html')

def actulizar_cuenta_usuario(request, id_usuario, id_persona):
    usuario= get_object_or_404(Usuario, pk=id_usuario)
    persona = get_object_or_404(Persona,pk=id_persona)
    formulario_persona= Formulario_persona(request.POST or None, instance=persona)
    usuario_formulario= Usuario_formulario_actulizar(request.POST or None, request.FILES or None, instance=usuario)
    if request.method=='POST':
        if formulario_persona.is_valid() and usuario_formulario.is_valid():
            formulario_persona.save()
            usuario= usuario_formulario.save(commit=False)
            usuario.persona=persona
            usuario.save()
            return redirect('listando_usuarios')
    context={
        'user':usuario,
        'persona':persona,
        'form_persona':formulario_persona,
        'form_usuario':usuario_formulario
    }
    detalle=f'Se ha editado el usuario: {usuario.username}'
    crear_log_sistema(request.user.username,'Edicion de Usuario', detalle ,'Usuario')
    return render(request, 'usuarios/actulizar_cuenta_formulario.html', context)

    

def creando_usuario(request):
    if(request.method=="POST"):
        formulario_u = Usuario_formulario(request.POST or None, request.FILES or None)
        formulario_p = Formulario_persona(request.POST)
        if formulario_u.is_valid() and  formulario_p.is_valid():
            persona= formulario_p.save()
            usuario= formulario_u.save(commit=False)
            password =formulario_u.cleaned_data['password']
            usuario.set_password(password)
            usuario.persona=persona
            usuario.save()
            detalle=f'Se ha creado una nuevo usuario: {usuario.username}'
            crear_log_sistema(request.user.username,'Creación de Usuarios', detalle ,'Usuario')
        else:
            formulario_u= Usuario_formulario(request.POST or None, request.FILES or None)
            formulario_p = Formulario_persona(request.POST)
    else:
        formulario_u= Usuario_formulario()
        formulario_p = Formulario_persona()
    context={'form_usuario':formulario_u,
             'form_persona':formulario_p,
             }
    return render(request, 'usuarios/crear_cuenta_formulario.html', context)


def crear_secretaria_listar(request):
    if(request.method == 'POST'):
        secretaria_post = request.POST.get('secretaria','').strip() 
        if not secretaria_post:
             return JsonResponse({"error":'este campo es obligatorio'})
        try:
            secretaria = Secretaria(secretaria=secretaria_post)
            secretaria.save()
            return JsonResponse({"data": True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})

    else:
        secretatias = list(Secretaria.objects.filter(esHabilitado=True).values())   
        return JsonResponse({'data':secretatias}, safe=False)
    
def Crear_unidad_secretaria(request):
    if request.method== 'POST':
        unidad = request.POST.get('unidad')
        id_secretaria = request.POST.get('secretaria_id')
        if not unidad and id_secretaria:
             return JsonResponse({'error':'campos obligatorios'})
        secretaria=get_object_or_404(Secretaria, pk=id_secretaria)
        try:
            unidad= Unidad.objects.create(nombre=unidad, secretaria=secretaria)
            unidad.save()
            oficina_exists = Oficinas.objects.filter(nombre='Ninguna').exists()
            if not oficina_exists:
                oficina= Oficinas.objects.create(nombre='Ninguna', unidad= unidad)
                oficina.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})
    
def crear_unidad_listar(request):
    if request.method == 'POST':
        unidad= request.POST['unidad']
        print(unidad)
        if not unidad:
            return JsonResponse({'error':'Este campo es obligatorio'})
        try:   
            unidad= Unidad.objects.create(nombre=unidad)
            unidad.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})
    else:
        unidad= list(Unidad.objects.filter(esHabilitado=True).values())
        return JsonResponse({'data':unidad})
    
    


def oficinas_listar(request, id_unidad):
    oficinas= list(Oficinas.objects.filter(unidad=id_unidad, esHabilitado=True).values())
    return JsonResponse({'data':oficinas})

def crear_oficinas(request):
    if request.method == 'POST':
        oficinas= request.POST['oficina']
        unidad= request.POST['unidad']
        if not oficinas:
            return JsonResponse({'error':'Este campo es obligatorio'})
        try:   
            unidad = get_object_or_404(Unidad, pk= unidad)
            oficinas= Oficinas.objects.create(nombre=oficinas, unidad=unidad)
            oficinas.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})






def listando_usuarios(request):
    pagina_actual = request.GET.get('page', 10)
    listado_cuentas_usuarios = Usuario.objects.select_related('persona').filter(es_habilitado=True)
    listado_cuentas_usuarios = paginador_general(request, listado_cuentas_usuarios, pagina_actual)
    print(listado_cuentas_usuarios)
    context={
        'data':listado_cuentas_usuarios,
       
    }
    return render(request, 'usuarios/mostrar_cuentas.html', context)

def soft_delete(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_habilitado=False
    usuario.save()
    detalle=f'Se ha eliminado el usuario: {usuario.username}'
    crear_log_sistema(request.user.username,'Eliminacion de Usuarios', detalle ,'Usuario')
    return redirect('listando_usuarios')

def desactivar_cuenta(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_activo= False
    usuario.save()
    detalle=f'Se ha desactivado el usuario: {usuario.username}'
    crear_log_sistema(request.user.username,'desactivacion de Usuario', detalle ,'Usuario')
    return redirect('listando_usuarios')

def activar_cuenta(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_activo= True
    usuario.save()
    detalle = f'El usuario {usuario.username} ha sido activado exitosamente.'
    crear_log_sistema(request.user.username, 'Activación de Usuario', detalle, 'Usuario')
    return redirect('listando_usuarios')

def logout_view(request):
    logout(request)
    return redirect('login')

def mi_perfil(request, id_usuario):
    return render(request,'usuarios/mi_perfil.html')

def buscar_cuenta(request, email):
    if not email:
        return  JsonResponse({'mensaje':'Ingrese su email'})
    
    cuentas = Usuario.objects.filter(email = email)
    cuentasEncontradas=[]
    for cuenta in cuentas:
        data={
            'id':cuenta.id,
            'nombres': cuenta.persona.nombre + cuenta.persona.nombre,
            'username':cuenta.username,
            'email':cuenta.email
        }
        cuentasEncontradas.append(data)
    if len(cuentasEncontradas) == 0:
         return  JsonResponse({'mensaje':'Cuenta no encontra'})
    return  JsonResponse({'data':cuentasEncontradas})


def cambiar_contrasena(request, id_usuario):
    user = get_object_or_404(Usuario, pk=id_usuario)
    if request.method =='POST':
        passw = request.POST['password']
        newPass= request.POST['confirm_password']
        if passw != newPass:
            mensaje='Las contrasena no son iguales'
            return render(request, 'usuarios/recetear.contrasena.html', {'mensaje':mensaje, 'id':id_usuario})
        elif not passw or not newPass:
            mensaje='Los campos son obligatorios'
            return render(request, 'usuarios/recetear.contrasena.html',{'mensaje':mensaje, 'id':id_usuario})
     
        user.set_password(passw)
        user.save()
        detalle = f'El usuario {user.username} ha sido canbiado su contraseña exitosamente.'
        crear_log_sistema(request.user.username, 'Cambio de contraseña', detalle, 'Usuario')
        return redirect('/')
    else:
        context={
        'id':id_usuario
        }
        return render(request, 'usuarios/recetear.contrasena.html', context)

def enviar_correos(request, id_usuario):
    user = get_object_or_404(Usuario, pk= id_usuario)
    email = user.email
    reset_link = request.build_absolute_uri(reverse('cambiar_contrasena', args=[user.id]))
    print(reset_link)
    template = get_template('usuarios/correos.html')

    context = {
        'user_name': user.persona.nombre +' '+ user.persona.apellidos , 
        'reset_link': reset_link, 
    }
    content = template.render(context)
   
    email_conf = EmailMultiAlternatives(
        subject='Recuperación de Contraseña',
        body='Este es el cuerpo en texto plano (opcional)',
        from_email=settings.EMAIL_HOST_USER,
        to=[email]
    )
    
    email_conf.attach_alternative(content, "text/html")
    
    try:
        email_conf.send()
        return JsonResponse({'data': True, 'mensaje':'Correo enviado'})
    except Exception as e:
        print(f'Error al enviar el correo: {e}')
        return JsonResponse({'data': False})
    
def listar_secretaria(request):
    secretarias = Secretaria.objects.filter(esHabilitado=True)
    context={
        'data':secretarias
    }
    return render(request,'usuarios/listar.secretarias.html', context) 
def listar_unidad(request):
    unidad = Unidad.objects.filter(esHabilitado=True)
    context={
        'data':unidad
    }
    return render(request,'usuarios/listar.unidades.html', context) 
def listar_oficina(request):
    oficinas = Oficinas.objects.filter(esHabilitado=True)
    context={
        'data':oficinas
    }
    return render(request,'usuarios/listar.oficinas.html', context)  
def soft_delete_secretaria(request, id):
    secretaria = get_object_or_404(Secretaria, pk=id)
    secretaria.esHabilitado=False
    secretaria.save()
    return redirect('listar_secretaria')

def soft_delete_undiad(request, id):
    unidad = get_object_or_404(Unidad, pk=id)
    unidad.esHabilitado=False
    unidad.save()
    return redirect('listar_unidad')
def soft_delete_oficina(request, id):
    oficina = get_object_or_404(Oficinas, pk=id)
    oficina.esHabilitado=False
    oficina.save()
    return redirect('listar_oficina')



def organigrama(request):
    data = []
    
    secretarias = Secretaria.objects.filter(esHabilitado=True)
    for se in secretarias:
        filtrado = {
            'secretaria': se.secretaria,
            'unidades': []
        }
        
        unidades = Unidad.objects.filter(esHabilitado=True, secretaria=se)
        for u in unidades:
            oficina_list = []
            oficinas = Oficinas.objects.filter(esHabilitado=True, unidad=u)
            for o in oficinas:
                oficina_list.append(o.nombre)
            
            filtrado['unidades'].append({
                'unidad': u.nombre,
                'oficinas': oficina_list
            })

        data.append(filtrado)

 
    
    return render(request, 'usuarios/organigrama.html', {'data': data})

def encrypt_file(file_path, output_path, key):

    key = key.ljust(32, b'\0')[:32]  
    iv = os.urandom(16) 
    

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
   
    with open(file_path, 'rb') as f:
        data = f.read()
    

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
 
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
 
    with open(output_path, 'wb') as f_enc:
        f_enc.write(iv + encrypted_data)  

def backup_database(request):
    print(os.getenv('DB_HOST'))
    if request.method == 'POST':
        try:
     
            temp_backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not os.path.exists(temp_backup_dir):
                os.makedirs(temp_backup_dir)

            # Nombre del archivo de backup
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup_file = os.path.join(temp_backup_dir, f'backup_{date_str}.sql')

       
            downloads_dir = os.path.join(str(Path.home()), 'Documents')
            final_backup_file_encrypted = os.path.join(downloads_dir, f'backup_{date_str}.enc')

            pg_dump_path = r'C:\Program Files\PostgreSQL\16\bin\pg_dump.exe'

            if not os.path.exists(pg_dump_path):
                return JsonResponse({'success': False, 'message': f'pg_dump no se encuentra en la ruta especificada: {pg_dump_path}'})

        
            command = [
                pg_dump_path,
                '-h', os.getenv('DB_HOST'),
                '-U', os.getenv('DB_USER'),
                '-d', os.getenv('DB_NAME'),
                '-f', temp_backup_file
            ]

        
            env = os.environ.copy()
            env['PGPASSWORD'] = settings.DATABASES["default"]["PASSWORD"]

        
            result = subprocess.run(command, env=env, text=True, capture_output=True)

         
            if result.returncode != 0:
                return JsonResponse({'success': False, 'message': f'Error al ejecutar pg_dump: {result.stderr}'})

           
            encryption_key = b'MySecretEncryptionKey'  # Usar una clave segura
            encrypt_file(temp_backup_file, final_backup_file_encrypted, encryption_key)


            os.remove(temp_backup_file)

      
            response = FileResponse(open(final_backup_file_encrypted, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(final_backup_file_encrypted)}"'
            return response

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear la copia de seguridad: {str(e)}'})

    else:
        return render(request, 'usuarios/backup.html')


def editar_secretaria(request, id):
    secretaria = get_object_or_404(Secretaria, pk = id)
    if request.method =='POST':
        secre = request.POST['secretaria']
        secretaria.secretaria= secre
        secretaria.save()
        return redirect('listar_secretaria')
    else:
        context={
            'secretaria':secretaria
        }
        return render(request, 'usuarios/editar.secretaria.html', context)
def editar_oficina(request, id):
    oficina = get_object_or_404(Oficinas, pk = id)
    if request.method =='POST':
        ofi = request.POST['oficina']
     
        oficina.nombre= ofi
        oficina.save()
        return redirect('listar_oficina')
    else:
        context={
            'oficina':oficina
        }
        return render(request, 'usuarios/editar.oficina.html',context)
def editar_unidad(request, id):
    unidad = get_object_or_404(Unidad, pk = id)
    if request.method =='POST':
        u = request.POST['unidad']
        unidad.nombre= u
        unidad.save()
        return redirect('listar_unidad')
    else:
        context={
            'unidad':unidad
        }
        return render(request, 'usuarios/editar.unidad.html', context)


def ayuda_tecnica(request):
    return render(request, 'usuarios/mantenimiento.html')
def manual_usuario(request):
    return render(request, 'usuarios/manual.html')