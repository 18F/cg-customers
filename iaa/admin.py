from django.contrib import admin
from .models import IAA, IAACommentInline

@admin.register(IAA)
class IAAAdmin(admin.ModelAdmin):
    inlines = [IAACommentInline]
    list_display = [f.name for f in IAA._meta.fields if f.name != "id"]
