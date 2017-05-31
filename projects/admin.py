from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from reversion.admin import VersionAdmin
from .models import Project, ProjectCommentInline

@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    list_display = ('project_name', 'agency', 'system_owner', 'iaa_link', 'package_link',)
    inlines = [ProjectCommentInline,]
    def iaa_link(self, obj):
        link = urlresolvers.reverse('admin:iaa_iaa_change', args=[obj.iaa_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.iaa) if obj.iaa else None
    def package_link(self, obj):
        link = urlresolvers.reverse('admin:packages_package_change', args=[obj.package_type_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.package_type) if obj.package_type else None
