from django.contrib import admin
from .models import IAA, IAAAdmin

admin.site.register(IAA, IAAAdmin)
