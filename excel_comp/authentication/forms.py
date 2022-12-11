from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Metal:
        model = User
        fields = ('email','username')
        # help_texts = {
        #     'username': None,
        #     'email': None,
        #     'password1':None,
        # }

    def save(self, commit=True ):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



    