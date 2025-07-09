from django import forms
from .models import VisionlineOperator
import base64

class VisionlineOperatorForm(forms.ModelForm):
    password_assigned = forms.CharField(
        label="Password assigned",
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        help_text="Se guardará cifrado en base64."
    )

    class Meta:
        model = VisionlineOperator
        fields = [
            "request_date", "full_name", "position", "eid", "department",
            "access_required", "setup_by", "completion_date",
            "username_assigned", "password_assigned", "is_active",
            "manager_signed", "request_pdf"
        ]
        widgets = {
            "request_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "eid": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "access_required": forms.Select(attrs={"class": "form-select"}),
            "setup_by": forms.TextInput(attrs={"class": "form-control"}),
            "completion_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "username_assigned": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "manager_signed": forms.TextInput(attrs={"class": "form-control"}),
            "request_pdf": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_password_assigned(self):
        password = self.cleaned_data["password_assigned"]
        return base64.b64encode(password.encode("utf-8")).decode("utf-8")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance