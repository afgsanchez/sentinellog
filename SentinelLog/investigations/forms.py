from django import forms
from .models import (
    InvestigationCase,
    InvestigationDocument,
    InvestigationComment,
    InterviewRecord
)

class InvestigationCaseForm(forms.ModelForm):
    class Meta:
        model = InvestigationCase
        fields = ['title', 'description', 'is_closed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del caso'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del caso',
                'rows': 4
            }),
        }

class InvestigationDocumentForm(forms.ModelForm):
    class Meta:
        model = InvestigationDocument
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del documento',
                'rows': 3,
                'style': 'height: 80px;'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class InvestigationCommentForm(forms.ModelForm):
    class Meta:
        model = InvestigationComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí',
                'rows': 4,
                'style': 'height: 100px;'  # Ajusta la altura para floating label
            }),
        }

class InterviewRecordForm(forms.ModelForm):
    class Meta:
        model = InterviewRecord
        fields = ['person_name', 'role', 'summary', 'date']
        widgets = {
            'person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la persona'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rol'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Resumen de la entrevista',
                'rows': 3,
                'style': 'height: 80px;'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
