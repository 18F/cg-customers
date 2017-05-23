from django.contrib import admin
from .models import Package, PackageAdmin

admin.site.register(Package, PackageAdmin)
