from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

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
