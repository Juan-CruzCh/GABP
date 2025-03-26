from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginador_general(request, lista_model, items_por_pagina):
    page = request.GET.get('page', 1)  

    paginador = Paginator(lista_model, items_por_pagina)  

    try:
        paginador_model = paginador.page(page) 
    except PageNotAnInteger:
 
        paginador_model = paginador.page(1)
    except EmptyPage:
   
        paginador_model = paginador.page(paginador.num_pages)

    return paginador_model
