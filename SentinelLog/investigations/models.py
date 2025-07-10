from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class InvestigationCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    conclusiones = models.TextField(blank=True, null=True)
    pdf_last_saved = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

class InvestigationDocument(models.Model):
    case = models.ForeignKey(InvestigationCase, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='investigations/documents/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InvestigationComment(models.Model):
    case = models.ForeignKey(InvestigationCase, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class InterviewRecord(models.Model):
    case = models.ForeignKey(InvestigationCase, on_delete=models.CASCADE, related_name='interviews')
    person_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    summary = models.TextField()
    conducted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
