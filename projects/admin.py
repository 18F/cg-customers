from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from reversion.admin import VersionAdmin
from .models import Project, ProjectCommentInline, QuotaHistory, PackageHistory

class PackageHistoryInline(admin.TabularInline):
    model = PackageHistory
    verbose_name = "Package History"
    verbose_name_plural = "Package History"
    extra = 1

class QuotaHistoryInline(admin.TabularInline):
    model = QuotaHistory
    verbose_name = "Quota History"
    verbose_name_plural = "Quota History"
    extra = 1

@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    list_display = ('project_name', 'agency', 'system_owner', 'iaa_link',)
    inlines = [PackageHistoryInline, QuotaHistoryInline, ProjectCommentInline,]
    def iaa_link(self, obj):
        link = urlresolvers.reverse('admin:iaa_iaa_change', args=[obj.iaa_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.iaa) if obj.iaa else None
