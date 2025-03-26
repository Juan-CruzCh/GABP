from django import forms
from .models import Categoria, Materiales, Informacion_material
from proveedor.models import Proveedor
class Formulario_materiales(forms.ModelForm):
    class Meta:
        model=Materiales
        fields = ['nombre','proveedor', 'codigo','factura','codigo_paquete' , 'marca',   'tamaño', 'color', 'unidad_medida','unidad_manejo','precio_unidad','precio_paquete', 'material', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'factura': forms.TextInput(attrs={'class': 'form-control'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_manejo': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_paquete': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_paquete':forms.TextInput(attrs={'class': 'form-control'}),
        
        }
     
    def __init__(self, *args, **kwargs):#mostrando en un select todas las categorias disponibles
        super(Formulario_materiales,self).__init__(*args, **kwargs)
        categorias_disponibles = [(categoria.id, categoria.nombre) for categoria in Categoria.objects.filter(es_habilitado=True)]#consultado a la base de datos   
        proveedores = [(proveedor.id, f'{proveedor.persona.nombre} {proveedor.persona.apellidos}') for proveedor in Proveedor.objects.filter(es_habilitado=True)]#consultado a la base de datos     
   
        self.fields['categoria'].widget = forms.Select(choices=categorias_disponibles, attrs={'class': 'form-select'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})

        self.fields['proveedor'].widget = forms.Select(choices=proveedores, attrs={'class': 'form-select'})
        self.fields['proveedor'].widget.attrs.update({'class': 'form-select'})
      

        instance = kwargs.get('instance')
        if instance:
            # Establecer campos de solo lectura
            self.fields['codigo'].widget.attrs['readonly'] = True
            self.fields['codigo_paquete'].widget.attrs['readonly'] = True
class Formulario_categoria(forms.ModelForm):
    class Meta:
        model=Categoria
        fields =['nombre','codigo_clasificacion']
        widgets = {
            'codigo_clasificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Form_infomacion_material(forms.ModelForm):
    class Meta:
        model= Informacion_material
        fields= ['cantidad_paquete', 'cantidad_paquete_unidad']
        widgets = {
            'cantidad_paquete': forms.TextInput(attrs={'class': 'form-control',}),
            'cantidad_paquete_unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_paquete': forms.TextInput(attrs={'class': 'form-control'}),
           'precio_unidad': forms.TextInput(attrs={'class': 'form-control'}),
        }
