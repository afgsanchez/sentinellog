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

class InvestigationCommentForm(forms.ModelForm):
    class Meta:
        model = InvestigationComment
        fields = ['comment']

class InterviewRecordForm(forms.ModelForm):
    class Meta:
        model = InterviewRecord
        fields = ['person_name', 'role', 'summary', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
