from django.db import models
from packages.models import Package

class Project(models.Model):
    agency = models.CharField(max_length=16, verbose_name="Agency")
    project_name = models.CharField(max_length=128, verbose_name="Project Name")
    org_manager = models.CharField(max_length=64, verbose_name="Org Manager")
    iaa_agreement = models.CharField(max_length=64, verbose_name="IAA Agreement")
    system_owner = models.CharField(max_length=64, verbose_name="System Owner")
    package_type = models.ForeignKey(Package)
    quota_memory_limit = models.PositiveIntegerField(verbose_name="Quota Memory Limit (in GB)")
    is_free = models.BooleanField(default=False)
