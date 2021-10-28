from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserEditForm(UserChangeForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

