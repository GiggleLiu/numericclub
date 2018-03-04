from django import forms

from .models import AdvancedUser


class LoginForm(forms.Form):
    class Meta:
        model = AdvancedUser
        fields = ('email', 'password')

class NewUserForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = ('username', 'email', 'password', 'description', 'avatar')


class UpdatePasswordForm(forms.Form):
    newpassword = forms.CharField(max_length=32)
    oldpassword = forms.CharField(max_length=32)

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = ('username', 'email', 'description', 'avatar')
