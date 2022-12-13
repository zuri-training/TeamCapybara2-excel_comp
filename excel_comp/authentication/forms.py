from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'id':'signin-email','placeholder':'Email :'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'signin-email','placeholder':'Username :'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password :','id':'signin-pwd'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password :','id':'signin-pwd'}))
    class Metal:
        model = User
        fields = ('email','username')
        # help_texts = {


    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



    