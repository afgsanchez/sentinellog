from django import forms
from .models import (
    Proveedor,
    CategoriaProveedor,
    Presupuesto,
    NotificacionInterna,
    AdjuntoPresupuesto
)

class CategoriaProveedorForm(forms.ModelForm):
    class Meta:
        model = CategoriaProveedor
        fields = ['nombre']

class ProveedorForm(forms.ModelForm):
    nueva_categoria = forms.CharField(
        required=False,
        label="Nueva categoría",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Servicios técnicos'
        })
    )

    class Meta:
        model = Proveedor
        fields = [
            'nombre', 'categoria', 'cif', 'direccion',
            'telefono', 'email', 'persona_contacto'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'cif': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'persona_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        nueva_categoria = cleaned_data.get('nueva_categoria')

        if categoria and nueva_categoria:
            raise forms.ValidationError(
                "Por favor, selecciona una categoría existente o escribe una nueva, pero no ambas."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        nueva_categoria = self.cleaned_data.get('nueva_categoria')
        if nueva_categoria:
            categoria, _ = CategoriaProveedor.objects.get_or_create(nombre=nueva_categoria)
            instance.categoria = categoria
        if commit:
            instance.save()
        return instance



class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = [
            'proveedor', 'numero', 'fecha', 'subtotal',
            'documento', 'estado', 'fecha_entrega_estimada',
            'responsable', 'comentarios'
        ]
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 2025-001'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del responsable'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['fecha', 'fecha_entrega_estimada']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')



class NotificacionInternaForm(forms.ModelForm):
    class Meta:
        model = NotificacionInterna
        fields = ['mensaje', 'presupuesto', 'leido']

class AdjuntoPresupuestoForm(forms.ModelForm):
    class Meta:
        model = AdjuntoPresupuesto
        fields = ['presupuesto', 'archivo', 'descripcion']
