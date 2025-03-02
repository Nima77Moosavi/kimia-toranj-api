from django.contrib import admin
from .models import Highlight, HighlightMedia

@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(HighlightMedia)
class HighlightMediaAdmin(admin.ModelAdmin):
    list_display = ('highlight', 'media_type', 'created_at')