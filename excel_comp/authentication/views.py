from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


from authentication.models import Profile
from authentication.forms import UserRegistrationForm

import random
import string

def generate_otp():
    new_otp = ""
    for i in range(6):
        new_otp += "".join(random.choice(string.digits))
    return new_otp

def validate_otp(user,otp):
    user = get_object_or_404(User,id=user)
    user_profile = get_object_or_404(Profile,user=user)
    if otp == user_profile.otp:
        user_profile.is_verified = True
        user_profile.save()
        return True
    return False


class RegisterView(generic.View):
    template_name = 'registration/signup.html'
    def get(self,request,*args,**kwargs):
        form = UserRegistrationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = UserRegistrationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('verify_account'))
        else:
            print(form.errors)
            return render(request,self.template_name,context)
           

class AccountValidationView(generic.View):
    template_name = 'registration/verify_account.html'
    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        otp = request.POST.get('otp')
        user = request.user.id
        if validate_otp(user,otp):
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,self.template_name,{'error':'incorrect codes entered try again!'})


class LoginView(generic.View):
    template_name = 'registration/login.html'
    def get(self,request,*args,**kwargs):
        form = AuthenticationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = AuthenticationForm(request.POST)
        context = {'form':form}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print('I am in')
            login(request,user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print('None User')
            return render(request,self.template_name,context)


class PasswordResetView(generic.View):
    template_name = 'authentication/recover_password.html'
    def get(self,request,*args,**kwargs):
        form = PasswordResetForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
            print('Form failed validations')
        context = {'form':form}
        return render(request,self.template_name,context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')