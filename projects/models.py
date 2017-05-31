from customer_admin.models import Comment, CommentInline
from django.db import models

class Project(models.Model):
    agency = models.CharField(max_length=16, verbose_name="Agency")
    project_name = models.CharField(max_length=128, verbose_name="Project Name")
    org_manager = models.CharField(max_length=64, verbose_name="Org Manager")
    iaa = models.ForeignKey('iaa.IAA', null=True, verbose_name="IAA")
    system_owner = models.CharField(max_length=64, verbose_name="System Owner")
    package_type = models.ForeignKey('packages.Package')
    quota_memory_limit = models.PositiveIntegerField(verbose_name="Quota Memory Limit (in GB)")
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return 'Project: {}'.format(self.project_name)

class ProjectComment(Comment):
    project = models.ForeignKey('Project')

class ProjectCommentInline(CommentInline):
    model = ProjectComment
