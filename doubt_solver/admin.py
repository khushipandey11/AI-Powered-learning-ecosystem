from django.contrib import admin
from .models import Doubt

@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at']
