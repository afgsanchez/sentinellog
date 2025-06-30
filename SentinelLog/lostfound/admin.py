from django.contrib import admin
from .models import LostFoundItem, LostFoundNote


class LostFoundNoteInline(admin.TabularInline):
    model = LostFoundNote
    extra = 1  # Muestra un formulario vacío extra para añadir notas


@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'found_at', 'found_on', 'status', 'returned_to', 'returned_on')
    list_filter = ('status', 'found_at', 'found_on')
    search_fields = ('description', 'found_at', 'returned_to', 'notes')
    inlines = [LostFoundNoteInline]

@admin.register(LostFoundNote)
class LostFoundNoteAdmin(admin.ModelAdmin):
    list_display = ('item', 'note', 'created_by', 'created_at')
    search_fields = ('note', 'created_by__username', 'item__description')