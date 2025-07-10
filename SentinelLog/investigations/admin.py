from django.contrib import admin
from .models import (
    InvestigationCase,
    InvestigationDocument,
    InvestigationComment,
    InterviewRecord
)
from simple_history.admin import SimpleHistoryAdmin

class InvestigationDocumentInline(admin.TabularInline):
    model = InvestigationDocument
    extra = 1

class InvestigationCommentInline(admin.TabularInline):
    model = InvestigationComment
    extra = 1

class InterviewRecordInline(admin.TabularInline):
    model = InterviewRecord
    extra = 1

@admin.register(InvestigationCase)
class InvestigationCaseAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_closed', 'has_documents')

    inlines = [InvestigationDocumentInline, InvestigationCommentInline, InterviewRecordInline]

    @admin.display(boolean=True, description='Has Documents')
    def has_documents(self, obj):
        return obj.documents.exists()
