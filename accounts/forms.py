from django import forms
from .models import GuestEmail


class GuestForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = ('email',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm password', max_length=255, widget = forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('passwords must match')
        return data
