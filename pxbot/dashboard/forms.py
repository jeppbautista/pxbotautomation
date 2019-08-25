from django.forms import ModelForm, SelectDateWidget, CheckboxInput
from django import forms

from .models import User

ATTRS_PASS = {'type': 'password'}
ATTRS_DATE = {'class': 'datepicker', 'readonly':''}


class UserUpdateActiveForm(ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)


class UserEditForm(ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs=ATTRS_PASS))
    expiration = forms.DateField(widget=forms.TextInput(attrs=ATTRS_DATE))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'expiration',
        )


class UserCreateForm(ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs=ATTRS_PASS))
    expiration = forms.DateField(widget=forms.TextInput(attrs=ATTRS_DATE))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'expiration',
        )