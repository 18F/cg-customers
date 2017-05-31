from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.db import models
from .forms import UserCreationForm, UserChangeForm

class Comment(models.Model):
    """
    Common comment model.
    """
    class Meta:
        abstract = True
    def __str__(self):
        return 'Date: {} | Comment: {}'.format(self.created_on, self.note)
    note = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class CommentInline(admin.TabularInline):
    """
    The base class for all comment inline classes.
    """
    extra = 0

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
