from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    # attrs for style
    # reference: https://docs.djangoproject.com/en/2.1/ref/forms/widgets/
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # set input type as password
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password do not match")
        return cd['password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'birth')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('school', 'company', 'profession', 'address', 'about', 'photo')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
