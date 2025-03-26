from datetime import datetime
from django.shortcuts import render

from logs.models import Logs_sistema
from utils.paginador import paginador_general


def crear_log_sistema(user, accion, detalle, modelo):
    Logs_sistema.objects.create(user=user ,
            accion=accion,
            detalle=detalle,
            modelo=modelo
            )
    return



def log_materiales(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
   
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        logs = Logs_sistema.objects.filter(modelo='Materiales',
                                            fecha__gte=fecha_inicio_dt,
                              fecha__lte=fecha_fin_dt
                                           )
        #pagina_actual = request.GET.get('limit', 10)
        #logs= paginador_general(request, logs, pagina_actual,)
        context={
        'data':logs
        }
        return render(request, 'logs/logs.sistema.materiales.html', context)
    return render(request, 'logs/logs.sistema.materiales.html')

def log_categorias(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
   
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        logs = Logs_sistema.objects.filter(modelo='Categoria',
                                            fecha__gte=fecha_inicio_dt,
                              fecha__lte=fecha_fin_dt
                                           )
        #pagina_actual = request.GET.get('limit', 10)
        #logs= paginador_general(request, logs, pagina_actual,)
        context={
        'data':logs
        }
        return render(request, 'logs/logs.sistema.categorias.html', context)
    return render(request, 'logs/logs.sistema.categorias.html')

def log_usuarios(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
   
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        logs = Logs_sistema.objects.filter(modelo='Usuario',
                                            fecha__gte=fecha_inicio_dt,
                              fecha__lte=fecha_fin_dt
                                           )
        #pagina_actual = request.GET.get('limit', 10)
        #logs= paginador_general(request, logs, pagina_actual,)
        context={
        'data':logs
        }
        return render(request, 'logs/logs.sistema.usuarios.html', context)
    return render(request, 'logs/logs.sistema.usuarios.html')

def log_pedidos(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
   
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        logs = Logs_sistema.objects.filter(modelo='Pedidos',
                                            fecha__gte=fecha_inicio_dt,
                              fecha__lte=fecha_fin_dt
                                           )
        #pagina_actual = request.GET.get('limit', 10)
        #logs= paginador_general(request, logs, pagina_actual,)
        context={
        'data':logs
        }
        return render(request, 'logs/logs.sistema.pedidos.html', context)
    return render(request, 'logs/logs.sistema.pedidos.html')

