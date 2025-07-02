
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from logs.views import crear_log_sistema
from utils.paginador import paginador_general
from .forms import Formulario_categoria,Formulario_materiales,Form_infomacion_material
from django.http import JsonResponse
from pedidos.models import Pedido

from datetime import datetime


from django.template.loader import get_template
from .models import Categoria, Materiales, Informacion_material
from django.contrib import messages

from django.db import transaction



def crear_categoria(request):    
    if(request.method == 'POST'):
        formulario= Formulario_categoria(request.POST)
        if formulario.is_valid():
            categoria=formulario.save()
            detalle=f'Se ha creado una nueva categoría: {categoria.nombre}'
            crear_log_sistema(request.user.username,'Creación de categoría', detalle ,'Categoria')
            return JsonResponse({'data':True})
        else:
            formulario= Formulario_categoria(request.POST)
            errors=  dict(formulario.errors.items())
            return JsonResponse({'errores':errors})
    else:
        formulario= Formulario_categoria()  
    categorias = Categoria.objects.filter(es_habilitado=True ).order_by('-fecha_creacion')
    context={
        'form':formulario,
        'categorias':categorias
    }
    return render(request, 'materiales/categoria/formulario.crear.html', context)

def crear_material(request):
    if(request.method=='POST'):
        fecha_actual = datetime.now()
        gestion = fecha_actual.year
        formulario= Formulario_materiales(request.POST)
        formulario_info_material= Form_infomacion_material(request.POST)
        if(formulario.is_valid() and formulario_info_material.is_valid()):
           try:
                codigo= formulario.cleaned_data['codigo']
                cantidad_paquete_unidad= formulario_info_material.cleaned_data['cantidad_paquete_unidad']
                precio_paquete= formulario_info_material.cleaned_data['precio_paquete']
              
                precio_unidad = precio_paquete / cantidad_paquete_unidad
                #codigo_paquete= formulario.cleaned_data['codigo_paquete']
                c = Materiales.objects.filter(codigo= codigo, es_habilitado=True).first()
                #p = Materiales.objects.filter(codigo_paquete= codigo_paquete,  es_habilitado=True).first()
                
                if c:
                    messages.success(request, f'El codigo {c.codigo}  ya existe')
                    return render(request, 'materiales/formulario.material.html', {'form': formulario, 'form_info': formulario_info_material})
                #elif p  :
                 #   messages.success(request, f'El codigo {p.codigo_paquete}  ya existe')
                  #  return render(request, 'materiales/formulario.material.html', {'form': formulario,'form_info': formulario_info_material })

                categoria= formulario.cleaned_data['categoria']
                cantidad_paquete= formulario_info_material.cleaned_data['cantidad_paquete']
         
                material= formulario.save(commit=False)
                
                material.codigo=f"{categoria.codigo_clasificacion}-{codigo }"
                material.stock= cantidad_paquete * cantidad_paquete_unidad
                material.gestion= gestion
                material.save()
                info_material= formulario_info_material.save(commit=False)
                info_material.material= material
                info_material.precio_unidad=precio_unidad
                info_material.save()
                info_material.calcular_total_cantidad()
                #info_material.calcular_precio_total()
                detalle=f'Se ha creado una nuevo material: {material.nombre} con el codigo {material.codigo}'
                crear_log_sistema(request.user.username,'Registrado', detalle ,'Materiales')
                messages.success(request, 'Material creado exitosamente.')
                return redirect('crear_material')
           except IntegrityError as e:
                print(e)
                if 'codigo_paquete' in str(e):
                    messages.error(request, 'El código de paquete ya existe.')
                else:
                    messages.error(request, 'El código de material ya existe.')
          
    else: 
        formulario= Formulario_materiales()
        formulario_info_material= Form_infomacion_material()
    context={
        'form':formulario,
        'form_info':formulario_info_material,
      
    }
    return render(request, 'materiales/formulario.material.html', context)


def listado_material(request, id_categoria):#lista todos los material por categoria
    fecha_actual = datetime.now()
    gestion = fecha_actual.year
    pagina_actual = request.GET.get('limit', 10)
    listar_productos_categoria= Materiales.objects.select_related('categoria').filter(categoria_id=id_categoria,es_habilitado=True, gestion = gestion, cierre_gestion=False)
    listar_productos_categoria=paginador_general(request, listar_productos_categoria, pagina_actual)
    nombre_categoria = Categoria.objects.get(pk=id_categoria)#trae el nombre de la categoria para el sud titulo
    context={
        'data':listar_productos_categoria,
        'nombre_categoria':nombre_categoria,
        'id_categoria':id_categoria
    }
    return render(request, 'materiales/listar_material.html', context)

def informacion_material(request, id_material):
    info_producto= Materiales.objects.get(pk= id_material)
    data_info_material =Informacion_material.objects.filter(material= id_material)

    context={
        'material':info_producto,
        'data_info_material':data_info_material
        
    }
    return render(request, 'materiales/informacion_material.html', context)

def editar_material(request, id_material):
    material = get_object_or_404(Materiales, pk=id_material)
    formulario_material = Formulario_materiales(request.POST or None, instance= material)
    if request.method == 'POST':
        if formulario_material.is_valid():
            codigo= formulario_material.cleaned_data['codigo']
            #codigo_paquete= formulario_material.cleaned_data['codigo_paquete']
            #antiguo_codigo_paquete=codigo_paquete.split('-')
            codigo_antiguo=codigo.split('-')
            categoria= formulario_material.cleaned_data['categoria']
            material= formulario_material.save()
            #material.codigo_paquete= f"{categoria.codigo_clasificacion}-{antiguo_codigo_paquete[1]}"
            material.codigo=codigo 
            material.save()
            detalle = f'Se ha editado el material con el código: {material.codigo}'
            crear_log_sistema(request.user.username,'Edicion', detalle ,'Materiales')
            messages.success(request, 'Material Editado exitosamente.')
            return redirect('editar_material', material.id)
    
    context={
        'form':formulario_material,
        'material': material

    }
    return render(request, 'materiales/formulario.actulizar.material.html', context)

def softDelete(request, id_material, id_categoria): #elimina el material
    material = get_object_or_404(Materiales, pk= id_material)
    categoria = get_object_or_404(Categoria, pk= id_categoria)
    material.es_habilitado= False
    material.save()
    detalle = f'Se ha eliminado el material con el código: {material.codigo}'
    crear_log_sistema(request.user.username,'Eliminacion', detalle ,'Materiales')
    return  redirect("categorias_por_id", id_categoria=categoria.id)



def inprimir(request, id):
    ruta_tamplate ='materiales/informacion_material.html'
    template = get_template(ruta_tamplate)
    mate = get_object_or_404(Materiales, pk=id)
    context = {'material': mate}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

def listar_categoria_id(request, id):
    categoria= get_object_or_404(Categoria, pk=id)
    data={
        'codigo':categoria.codigo_clasificacion,
        'nombre':categoria.nombre,
        'id':categoria.id
    }
    return JsonResponse(data)

def actualizar_categoria(request):
    id=request.POST['id']
    nombre=request.POST['nombre']
    codigo=request.POST['codigo']
    if not  nombre  or not id:
        return JsonResponse({'error':'Ingrese los campos'})
    try:
        categoria= get_object_or_404(Categoria, pk=id)
        nombre_anterior= categoria.nombre
        categoria.nombre =nombre
        categoria.codigo_clasificacion = codigo
        categoria.save()
        detalle=f"Se ha editado la categoría: {nombre_anterior} a {categoria.nombre}"
        crear_log_sistema(request.user.username,'Edicion', detalle ,'Categoria')
        return JsonResponse({'data':True})
    except IntegrityError as e:
        return JsonResponse({'error': 'La categoria ya existe'})



def eliminar_categoria(request, id):
    categoria= get_object_or_404(Categoria, pk=id)
    categoria.es_habilitado=False
    categoria.save()
    detalle=f"Se ha Elimando la categoría: {categoria.nombre}"
    crear_log_sistema(request.user.username,'Eliminacion', detalle ,'Categoria')
    return redirect('crear_categoria')

def anadir_nuevo_cantidad(request):
    cantidad_unidad= request.POST['cantidadUnidad']
    cantidad_paquete= request.POST['cantidadPaquete']
    precio_paquete= request.POST['precioPaquete']
    id_material=request.POST['materialId']
    #precio_unidad=request.POST['precio_unidad']
    if not cantidad_unidad or not cantidad_paquete or not id_material:
        return JsonResponse({'data':'Campos obligatorios'})
    totalCantidad = int(cantidad_unidad) * int(cantidad_paquete)
    material=get_object_or_404(Materiales, pk = id_material)
    precio_unidad = float(precio_paquete) /int(cantidad_unidad) 
    stock = material.stock
    material.stock= int(stock) + totalCantidad
    
    info_mat = Informacion_material.objects.create(precio_paquete=precio_paquete,precio_unidad=precio_unidad,cantidad_paquete= int(cantidad_paquete), cantidad_paquete_unidad= int(cantidad_unidad),material= material)
    info_mat.calcular_total_cantidad()
    #info_mat.calcular_precio_total()
    material.save()
    info_mat.save()
    detalle = f'Se registro una nueva cantidad al material con el código: {material.codigo}'
    crear_log_sistema(request.user.username,'Registro', detalle ,'Materiales')
    return JsonResponse({'data':True})

def reporte_materiales_entrada(request):
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
      
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)

        material = Informacion_material.objects.filter(
            fecha_creacion__gte= fecha_inicio_dt,
            fecha_creacion__lte= fecha_fin_dt,
            
        )
        context={
            'fecha_inicio':fecha_inicio,
            'fecha_fin':fecha_fin,
            'data':material
        }
        return render(request, 'materiales/reporte.material.entrada.html', context)


    return render(request, 'materiales/reporte.material.entrada.html')

def cerrar_gestion(request):
    fecha = datetime.now()
    gestionNueva = fecha.year
    if request.method == 'POST':
        gestion = request.POST['año']
        if gestion >= str(gestionNueva):
            messages.warning(request, 'Cierre de gestión negado. Asegúrate de ingresar el año correcto.')
            return redirect('cerrar_gestion')

        materiales = Materiales.objects.filter(gestion=gestion, es_habilitado=True, cierre_gestion=False)
        materiales_a_crear = []

        for m in materiales:
            if m.stock > 0:
                # Crear una copia con un nuevo ID y el año nuevo
                nuevos_material = Materiales(
                    nombre=m.nombre,
                    codigo=f"{m.codigo}{gestionNueva}",
                    marca=m.marca,
                    stock=m.stock,
                    tamaño=m.tamaño,
                    color=m.color,
                    unidad_medida=m.unidad_medida,
                    unidad_manejo=m.unidad_manejo,
                    material=m.material,
                    precio_unidad=m.precio_paquete,
                    precio_paquete=m.precio_paquete,
                    factura=m.factura,
                    codigo_paquete=f"{m.codigo_paquete}{gestionNueva}",
                    categoria=m.categoria,
                    proveedor=m.proveedor,
                    es_habilitado=m.es_habilitado,
                    gestion=gestionNueva,
                    cierre_gestion=False
                   
                )
                materiales_a_crear.append(nuevos_material)

        with transaction.atomic():
            Materiales.objects.bulk_create(materiales_a_crear)  # Crear todos los nuevos materiales
            materiales.update(cierre_gestion=True)  # Actualizar los materiales existentes

        messages.success(request, 'Cierre de gestión completada')
        context = {
            'selected_year': gestion,
        }
        return render(request, 'materiales/cerrar.gestion.html', context)

    return render(request, 'materiales/cerrar.gestion.html')
    
def reporte_gestion(request):
 
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
   
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
      
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
  
    
        materiales= Materiales.objects.filter(es_habilitado=True 
                                              , cierre_gestion=True,
                                                fecha_creacion__gte =fecha_inicio_dt,
                                                  fecha_creacion__lte =fecha_fin_dt
                                              )
  
        #materiales = paginador_general(request, materiales, pagina_actual)
      
        context={
            'data':materiales,
          
         }
        return render(request, 'materiales/reporte.gestion.html', context)

    return render(request, 'materiales/reporte.gestion.html')
    

def inventario_fisico(request):
    data = []
    pedidos = Pedido.objects.filter(aprobado_almacen=True)

    for p in pedidos:
        # Use filter() to retrieve all matching records for the given material_id
        cantidades = Informacion_material.objects.filter(material_id=p.material.id)
        cantidad = cantidades.first()  # This will return the first record or None if empty
        info = {
            'codigo': p.material.codigo,
            'nombre': p.material.nombre,
            'unidad_manejo': p.material.unidad_manejo,
            'compra': cantidad.cantidad if cantidad.cantidad else 0,  # If cantidad is None, default to 0
            'stock': p.material.stock,
            'entrega': p.cantidad_entrega,
            'cantidad2': p.material.stock + (cantidad.cantidad_paquete_unidad if cantidad else 0) - p.cantidad_entrega
        }
        data.append(info)

  
    context = {
        'data': data
    }
    return render(request, 'materiales/inventarioFisico.html', context)
