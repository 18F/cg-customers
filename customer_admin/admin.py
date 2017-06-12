from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email'),
        }),
    )

    form = UserChangeForm

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_superuser'),
        }),
    )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
