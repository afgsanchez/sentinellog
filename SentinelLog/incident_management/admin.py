from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin

class IncidentPhotoInline(admin.TabularInline):
    model = IncidentPhoto
    extra = 1

class IncidentNoteInline(admin.TabularInline):
    model = IncidentNote
    extra = 1

class IncidentAttachmentInline(admin.TabularInline):
    model = IncidentAttachment
    extra = 1

@admin.register(Incident)
class IncidentAdmin(SimpleHistoryAdmin):
    list_display = ('incident_type', 'date', 'location', 'reported_by', 'insurance_case_number', 'related_investigation')
    list_filter = ('incident_type', 'date', 'reported_by')
    search_fields = ('description', 'location', 'insurance_case_number')
    inlines = [IncidentPhotoInline, IncidentNoteInline, IncidentAttachmentInline]

admin.site.register(IncidentType)

# Si quieres, puedes registrar IncidentPhoto y IncidentNote por separado:
# admin.site.register(IncidentPhoto)
# admin.site.register(IncidentNote)