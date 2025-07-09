from django.contrib import admin
from .models import VisionlineOperator

@admin.register(VisionlineOperator)
class VisionlineOperatorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "eid", "department", "access_required",
        "username_assigned", "is_active", "request_date", "completion_date"
    )
    list_filter = ("is_active", "access_required", "department")
    search_fields = ("full_name", "eid", "username_assigned", "department")
    readonly_fields = ("created_at",)