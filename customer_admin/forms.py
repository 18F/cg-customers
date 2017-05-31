from django.contrib.auth.forms import UsernameField
from django.contrib.auth import get_user_model
from django.forms import EmailField
from django.forms import ModelForm

class UserCreationForm(ModelForm):
    """A replacement for user creation form which does not contain a
    password. Largely lifted from Django"""
    email = EmailField(label=("Email address"), required=True,
        help_text=("Required."))
    class Meta:
        model = get_user_model()
        fields = ("username", "email",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {'autofocus': True})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    email = EmailField(label=("Email address"), required=True,
        help_text=("Required."))
    """A replacement for user change which does not contain a password.
    Largely lifted from Django"""
    class Meta:
        model = get_user_model()
        exclude = ['is_staff', 'password']
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
