from django.contrib import admin
from .models import LostFoundItem

@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'found_at', 'found_on', 'status', 'returned_to', 'returned_on')
    list_filter = ('status', 'found_at', 'found_on')
    search_fields = ('description', 'found_at', 'returned_to', 'notes')