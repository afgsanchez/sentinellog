from django import forms
from .models import *

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'incident_type',
            'date',
            'location',
            'description',
            'reported_by',
            'incident_report_docx',
            'insurance_case_number',
            'related_investigation',
        ]
        widgets = {
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación del incidente'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del incidente'}),
            'reported_by': forms.Select(attrs={'class': 'form-select'}),
            'incident_report_docx': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'insurance_case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de caso de la aseguradora'}),
            'related_investigation': forms.Select(attrs={'class': 'form-select'}),
        }

from .models import IncidentNote
from django import forms

class IncidentNoteForm(forms.ModelForm):
    class Meta:
        model = IncidentNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Añade una nota sobre el incidente...'
            }),
        }


class IncidentPhotoForm(forms.ModelForm):
    class Meta:
        model = IncidentPhoto
        fields = ['image']

class IncidentAttachmentForm(forms.ModelForm):
    class Meta:
        model = IncidentAttachment
        fields = ['file', 'description']