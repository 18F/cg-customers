from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Package
@admin.register(Package)
class PackageAdmin(VersionAdmin):
    list_display = ('package_name', 'monthly_price',)
