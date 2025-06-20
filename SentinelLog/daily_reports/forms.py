from django import forms
from .models import DailyReport

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['report_type', 'date', 'pdf_file', 'related_case', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'related_case': forms.Select(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }