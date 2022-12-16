import email
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings

from authentication.models import Profile
from authentication.forms import UserRegistrationForm

import random
import string

def process_otp(input):
    result = ""
    for i in range(1,7):
        result += input[f"otp{i}"]
    return result


def send_otp_mail(recipient,code):
    subject = 'welcome to Excel_Comp '
    message = f'Hi {recipient.username}, thank you for registering in Excel_Comp. Kindly use the below code to verify your account \n{code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient.email, ]
    send_mail( subject, message, email_from, recipient_list )



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
    template_name = 'registration/otp.html'
    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        input = request.POST.dict()
        otp = process_otp(input)
        user = request.user.id
        if validate_otp(user,otp):
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,self.template_name,{'error':'incorrect codes entered try again!'})


def resend_otp(request):
    email = request.user.email
    user = get_object_or_404(User,email=email)
    code = generate_otp()
    send_otp_mail(user,code)
    return True
    
class RequestAuthenticationView(generic.View):
    template_name = 'registration/auth.html'
    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        email = request.user.email
        code = generate_otp()
        send_otp_mail(email,code)
  
            
        return render(request,self.template_name)



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
            print('User Logged In')
            login(request,user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print('User Fail')
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