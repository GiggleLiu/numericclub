from django import forms

from .models import AdvancedUser

class PasswordField(forms.CharField):
    widget = forms.PasswordInput

class LoginForm(forms.Form):
    class Meta:
        model = AdvancedUser
        fields = ('email', 'password')
        widgets = {
                'password': forms.PasswordInput(),
                }

class NewUserForm(forms.ModelForm):
    password2 = PasswordField(max_length=32, label='Repeat Password')
    class Meta:
        model = AdvancedUser
        fields = ('truename', 'email', 'password', 'description', 'avatar')
        widgets = {
                'password': forms.PasswordInput(),
                'description': forms.Textarea(attrs={'rows': '4'}),
                }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = ('truename', 'description', 'avatar')
        widgets = {
                'description': forms.Textarea(attrs={'rows': '4'}),
                }

class UpdatePasswordForm(forms.Form):
    newpassword = PasswordField(max_length=32, label='New Password')
    oldpassword = PasswordField(max_length=32, label='Old Password')
