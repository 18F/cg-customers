from customer_admin.models import Comment, CommentInline
from django.contrib import admin
from django.core import urlresolvers
from django.db import models
from django.utils.html import format_html
from packages.models import Package
from iaa.models import IAA

class Project(models.Model):
    agency = models.CharField(max_length=16, verbose_name="Agency")
    project_name = models.CharField(max_length=128, verbose_name="Project Name")
    org_manager = models.CharField(max_length=64, verbose_name="Org Manager")
    iaa = models.ForeignKey(IAA, null=True, verbose_name="IAA")
    system_owner = models.CharField(max_length=64, verbose_name="System Owner")
    package_type = models.ForeignKey(Package)
    quota_memory_limit = models.PositiveIntegerField(verbose_name="Quota Memory Limit (in GB)")
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return 'Project: {}'.format(self.project_name)

class ProjectComment(Comment):
    project = models.ForeignKey(Project)

class ProjectCommentInline(CommentInline):
    model = ProjectComment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'agency', 'system_owner', 'iaa_link', 'package_link',)
    inlines = [ProjectCommentInline]
    def iaa_link(self, obj):
        link = urlresolvers.reverse('admin:iaa_iaa_change', args=[obj.iaa_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.iaa) if obj.iaa else None
    def package_link(self, obj):
        link = urlresolvers.reverse('admin:packages_package_change', args=[obj.package_type_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.package_type) if obj.package_type else None
