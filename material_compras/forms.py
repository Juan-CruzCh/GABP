from django import forms

from usuarios.models import Oficinas, Unidad
from .models import Matarial_compras

class Form_material_compras(forms.ModelForm):
    class Meta:
        model = Matarial_compras
        fields = [
            'item', 'descripcion', 'orden_compra', 
            'unidad_manejo', 'fecha_compra', 'secretaria', 'unidad', 
            'oficina', 'proveedor', 'cantidad', 'costo_unitario', 
            'factura', 'costo_unitario'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del material',
                'rows': 3,
            }),
            'orden_compra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de orden de compra'
            }),
        
            'unidad_manejo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la unidad de manejo'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la fecha de compra',
                'type': 'date'
            }),
            'secretaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'unidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'oficina': forms.Select(attrs={
                'class': 'form-control'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad'
            }),
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el costo unitario'
            }),
            'factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de factura'
            }),
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Costo unitario'
            }),
          
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializa las listas de opciones vacías para evitar problemas
        self.fields['unidad'].queryset = Unidad.objects.none()
        self.fields['oficina'].queryset = Oficinas.objects.none()

        if 'secretaria' in self.data:
            try:
                secretaria_id = int(self.data.get('secretaria'))
                self.fields['unidad'].queryset = Unidad.objects.filter(secretaria_id=secretaria_id)
            except (ValueError, TypeError):
                pass

        if 'unidad' in self.data:
            try:
                unidad_id = int(self.data.get('unidad'))
                self.fields['oficina'].queryset = Oficinas.objects.filter(unidad_id=unidad_id)
            except (ValueError, TypeError):
                pass


        elif self.instance.pk:
            self.fields['unidad'].queryset = self.instance.secretaria.unidad_set.all()
            self.fields['oficina'].queryset = self.instance.unidad.oficina_set.all()