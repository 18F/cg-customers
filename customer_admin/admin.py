from django.contrib import admin

from django.contrib.auth.models import User
from . import forms

admin.site.unregister(User)
admin.site.register(User, forms.UserAdmin)
