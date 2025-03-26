from django.urls import path
from .views import vistar_administracion
urlpatterns = [
 path('administracion',vistar_administracion , name='administracion' ),

]