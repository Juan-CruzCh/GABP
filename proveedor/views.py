from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django_countries import countries ##sale de aqui todos los paises
from  persona.models import Persona
from .models import Proveedor
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from  utils.paginador import paginador_general

def listar_proveedores(request):
    pagina_actual = request.GET.get('page', 10)
    listar_proveedores = Proveedor.objects.select_related('persona').filter(es_habilitado=True)
    listar_proveedores= paginador_general(request, listar_proveedores, pagina_actual)

    return render(request, 'proveedor/index.html',{'data':listar_proveedores})


def formulario_proveedor(request):
    if(request.method == 'POST'):
        empresa = request.POST['empresa']
        nit = request.POST['nit']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        cedula_identidad = request.POST['cedula_identidad']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        pais = request.POST['pais'] 
        descripcion= request.POST['descripcion']
        ciudad= request.POST['ciudad']

        try:
            persona= Persona.objects.create(cedula_identidad= cedula_identidad, nombre= nombre, apellidos= apellidos)
            Proveedor.objects.create(empresa=empresa,ciudad= ciudad, descripcion= descripcion,nit= nit, correo= correo, telefono=telefono,pais=pais ,direccion= direccion, persona=persona)
            return redirect('listar_proveedor')
        except IntegrityError as err:
            mensaje= 'La cedula de identidad ya existe'
            return  render(request, 'proveedor/formulario.html', {'paises':countries,'mensaje':mensaje})
        
    return  render(request, 'proveedor/formulario.html', {'paises':countries})
def actulizar_proveedor(request, id):
    proveedor =get_object_or_404(Proveedor, pk=id)
    if request.method =='POST':
        empresa = request.POST['empresa']
        nit = request.POST['nit']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        cedula_identidad = request.POST['cedula_identidad']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        pais = request.POST['pais'] 
        descripcion= request.POST['descripcion']
        ciudad= request.POST['ciudad']

        try:
            proveedor.empresa= empresa
            proveedor.nit=nit
            proveedor.persona.nombre=nombre
            proveedor.persona.apellidos=apellidos
            proveedor.persona.cedula_identidad= cedula_identidad
            proveedor.correo=correo
            proveedor.telefono=telefono
            proveedor.direccion= direccion
            proveedor.pais=pais
            proveedor.descripcion=descripcion
            proveedor.ciudad=ciudad
            proveedor.save()
            proveedor.persona.save()
            mensaje= 'Actulizado'
            context={
                    'data': proveedor,
                    'paises':countries,
                    'mensaje':mensaje
                     }
            return  render(request, 'proveedor/actualizar.formulario.html', context)
        except IntegrityError:
                mensaje= 'La cedula de identidad ya existe'
                context={
                    'data': proveedor,
                    'paises':countries,
                    'mensaje':mensaje
                     }
                return  render(request, 'proveedor/actualizar.formulario.html', context)
 
    context={
    'data': proveedor,
       'paises':countries
        }
    return  render(request, 'proveedor/actualizar.formulario.html', context)

def softDelete(request, id):
    proveedor =get_object_or_404(Proveedor, pk=id)
    proveedor.es_habilitado=False
    proveedor.save()
    return redirect('listar_proveedor')
  