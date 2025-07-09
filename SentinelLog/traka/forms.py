from django import forms
from .models import TrakaKeyUser

class TrakaKeyUserForm(forms.ModelForm):
    class Meta:
        model = TrakaKeyUser
        fields = [
            "nombre", "cargo", "departamento", "sistema", "tipo_llave",
            "posicion", "acceso_anterior", "solicitud_pdf", "activo"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cargo": forms.TextInput(attrs={"class": "form-control"}),
            "departamento": forms.Select(attrs={"class": "form-select"}),
            "sistema": forms.Select(attrs={"class": "form-select"}),
            "tipo_llave": forms.Select(attrs={"class": "form-select"}),
            "posicion": forms.NumberInput(attrs={"class": "form-control"}),
            "acceso_anterior": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "solicitud_pdf": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
