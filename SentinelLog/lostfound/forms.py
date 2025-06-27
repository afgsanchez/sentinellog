from django import forms
from .models import LostFoundItem, LostFoundNote

class LostFoundItemForm(forms.ModelForm):
    class Meta:
        model = LostFoundItem
        fields = [
            'description',
            'found_at',
            'found_on',
            'found_by',
            'photo',
            'status',
            'returned_to',
            'returned_on',
            'notes',
        ]
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del objeto'}),
            'found_at': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar donde se encontró'}),
            'found_on': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'found_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿Quién encontró el objeto?'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'returned_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona a la que se entrega (si aplica)'}),
            'returned_on': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales'}),
        }



class LostFoundNoteForm(forms.ModelForm):
    class Meta:
        model = LostFoundNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Añade una nota sobre el objeto...'
            }),
        }