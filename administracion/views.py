from django.shortcuts import render



def vistar_administracion(request):#vist
    prueba='hola'
    return render(request, 'administracion/administracion.html')
