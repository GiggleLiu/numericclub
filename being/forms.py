from django import forms
from django.contrib.auth.models import User
from being.models import Being


class LoginForm(forms.Form):
    name = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UpdatePasswordForm(forms.Form):
    newpassword = forms.CharField(max_length=32)
    oldpassword = forms.CharField(max_length=32)


class UpdateBeingForm(forms.ModelForm):
    class Meta:
        model = Being
        fields = ('description', 'avatar', 'truename')
        widgets = {
            'description': forms.Textarea(attrs={'rows': '4'}),
        }


class NewBeingForm(forms.ModelForm):
    class Meta:
        model = Being
        fields = ('avatar', 'description', 'truename')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '10'}),
        }


class UpdateUserForm(forms.ModelForm):
    oldpassword = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('password', 'email')
