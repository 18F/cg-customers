from customer_admin.models import Comment, CommentInline
from django.db import models


class PackageHistory(models.Model):
    project = models.ForeignKey('Project')
    package_type = models.ForeignKey('packages.Package')
    start_date = models.DateField(verbose_name="Package Effective Start Date")
    end_date = models.DateField(verbose_name="Package Effective End Date", null=True)

    def __str__(self):
        return 'Package: {} starting on {}'.format(self.package_type.package_name, self.start_date)

class QuotaHistory(models.Model):
    project = models.ForeignKey('Project')
    quota_memory_limit = models.PositiveIntegerField(verbose_name="Quota Memory Limit (in GB)")
    start_date = models.DateField(verbose_name="Quota Effective Start Date", help_text="")
    end_date = models.DateField(verbose_name="Quota Effective End Date", null=True)

    def __str__(self):
        return 'Quota: {}GB starting on {}'.format(self.quota_memory_limit, self.start_date)

class Project(models.Model):
    agency = models.CharField(max_length=16, verbose_name="Agency")
    project_name = models.CharField(max_length=128, verbose_name="Project Name")
    org_manager = models.CharField(max_length=64, verbose_name="Org Manager")
    iaa = models.ForeignKey('iaa.IAA', null=True, verbose_name="IAA")
    system_owner = models.CharField(max_length=64, verbose_name="System Owner")
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return 'Project: {}'.format(self.project_name)

class ProjectComment(Comment):
    project = models.ForeignKey('Project')

class ProjectCommentInline(CommentInline):
    model = ProjectComment
