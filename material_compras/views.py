from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from material_compras.forms import  Form_material_compras 
from material_compras.models import Matarial_compras, Numero_registro ,Pedido_compras
from usuarios.models import Oficinas, Unidad
from proveedor.models import Proveedor
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

@csrf_exempt
def crear_material_compras(request):

    form_compras = Form_material_compras(request.POST or None)
    print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        materiales = data.get("materiales", [])
        numero = Numero_registro.objects.create()
        for mat in materiales:
            proveedor = get_object_or_404(Proveedor, pk= mat["proveedorId"])
            unidad = get_object_or_404(Unidad, pk= mat["unidadId"])
            Matarial_compras.objects.create(
                    item=mat["item"],
                    descripcion=mat["descripcion"],
                    unidad_manejo=mat["unidad"],
                    cantidad=mat["cantidad"],
                    costo_unitario=mat["costo"],
                    fecha_compra=mat["fecha"],
                    proveedor = proveedor,
                    unidad= unidad,
                    numero_registro= numero,
                      estado_compra='COMPLETADO',
                    costo_total= int(mat["cantidad"]) * float(mat["costo"])

                )

        return JsonResponse({"data": True,'numero':numero.pk})
             

    context = {
        'form': form_compras,
      
       
    }
    return render(request, 'material_compras/crear.html', context)



def listar_compras():
    compra= Matarial_compras.objects.filter(estado_compra='PENDIENTE')
    return  compra

def listar_material_compras(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        print(fecha_inicio_dt,fecha_fin_dt)
        material = Matarial_compras.objects.filter(flag=True,            
                                                  fecha_creacion__gte=fecha_inicio_dt,
                              fecha_creacion__lte=fecha_fin_dt,
                                 estado_compra='COMPLETADO'
                              )
        context={
            'data':material
        }
        return render(request, 'material_compras/listar.html', context)
    return render(request, 'material_compras/listar.html')

def listar_material_compras_user(request):
    user= request.user
  
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        material = Pedido_compras.objects.filter(           
                                                  fecha_creacion__gte=fecha_inicio_dt,
                              fecha_creacion__lte=fecha_fin_dt,
                              
                              )
        context={
            'data':material
        }
        return render(request, 'material_compras/secretaria.html', context)
    return render(request, 'material_compras/secretaria.html')



def cargar_unidades(request):
    secretaria_id = request.GET.get('secretaria')
    unidades = Unidad.objects.filter(secretaria_id=secretaria_id).values('id', 'nombre')
    return JsonResponse(list(unidades), safe=False)

def cargar_oficinas(request):
    unidad_id = request.GET.get('unidad')
    oficinas = Oficinas.objects.filter(unidad_id=unidad_id).values('id', 'nombre')
    return JsonResponse(list(oficinas), safe=False)


def guardar_material_compras(request):
    numero = Numero_registro.objects.create()
    material =Matarial_compras.objects.filter(estado_compra='PENDIENTE')
    print(material)
    for m in material:
        m.estado_compra='COMPLETADO'
        m.numero_registro=numero
        m.save()
    return JsonResponse({'data':'Registrado'})

def eliminar(request,id):
    material= get_object_or_404(Matarial_compras, pk=id)
    material.delete()
    return JsonResponse({'data':True})


def verificar(request,id):
    pedido_compras= get_object_or_404(Pedido_compras, pk=id)
    fecha = datetime.now()
    pedido_compras.fecha_cardista= fecha
    pedido_compras.estado_cardista= True
    pedido_compras.save()
    return redirect('secreatria_material')
    


def realizar_entrega(request):
        
        if request.method =='POST':
            cantidad_entrega = request.POST['cantidad_entrega']
            id = request.POST['id']
            material_compras = get_object_or_404(Matarial_compras, pk= id)
            nueva_cantidad = int(material_compras.cantidad) - int(cantidad_entrega)
            material_compras.cantidad=nueva_cantidad
         
            Pedido_compras.objects.create(cantidad_entrega= cantidad_entrega , material_compras = material_compras)
            material_compras.save()
            return JsonResponse({'data':True})

def listar_material_compras_entregadas(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)

        pedidos = Pedido_compras.objects.filter(            
                                                  fecha_cardista__gte=fecha_inicio_dt,
                              fecha_cardista__lte=fecha_fin_dt,
                            
                              )
        for pedido in pedidos:
            pedido.costo_total = pedido.material_compras.costo_unitario * pedido.cantidad_entrega
        context={
            'data':pedidos
        }
        return render(request, 'material_compras/entregados.html', context)
    return render(request, 'material_compras/entregados.html')
def entrada(request, numero):
    numero = get_object_or_404(Numero_registro, pk=numero)
    material = Matarial_compras.objects.filter(numero_registro=numero)
    total = material.aggregate(total=Sum('costo_total'))['total'] or 0
    return render(request, 'material_compras/entrada.pdf.html', {
        'materiales': material,
        'numero': numero,
        'total':total
    })