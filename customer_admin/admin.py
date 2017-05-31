from django.contrib import admin

from django.contrib.auth import get_user_model
from .models import UserAdmin

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
