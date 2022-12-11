from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


from authentication.models import Profile
from authentication.forms import UserRegistrationForm


def validate_otp(user,otp):
    user = get_object_or_404(User,id=user)
    user_profile = get_object_or_404(Profile,user=user)
    if otp == user_profile.otp:
        user_profile.is_verified = True
        user_profile.save()
        return True
    return False


class RegisterView(generic.View):
    template_name = 'authentication/index.html'
    def get(self,request,*args,**kwargs):
        form = UserRegistrationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = UserRegistrationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('account_validation'))
            else:
                return render(request,self.template_name,context)
        else:
            return render(request,self.template_name,context)
           

class AccountValidationView(generic.View):
    template_name = 'authentication/validate_email.html'
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
    template_name = 'authentication/index.html'
    def get(self,request,*args,**kwargs):
        form = AuthenticationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('email_validation'))
            else:
                return render(request,self.template_name,context)
        else:
            context = {'form':form}
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
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            print('Form failed validations')
        context = {'form':form}
        return render(request,self.template_name,context)