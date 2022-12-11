from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm

from authentication.forms import UserRegistrationForm

class LoginRegisterView(generic.View):
    template_name = 'authentication/index.html'
    def get(self,request,*args,**kwargs):
        form = UserRegistrationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            print('Form failed validations')
        context = {'form':form}
        return render(request,self.template_name,context)

class LoginRegisterView(generic.View):
    template_name = 'authentication/index.html'
    def get(self,request,*args,**kwargs):
        form = AuthenticationForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            print('Form failed validations')
        context = {'form':form}
        return render(request,self.template_name,context)

def home(request):
   
    return render(request,'authentication/home.html')

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

# class IndexView(generic.View):
#     template_name = 'core/login.html'
#     def get(self,*args,**kwargs):
     
#         form = CustomerForm()
#         login_form = LoginForm()
#         context = {'form':form,'login_form':login_form,'disp':False}

#         return render(self.request,self.template_name,context=context)
    
#     def post(self,*args,**kwargs):
#         form = CustomerForm(self.request.POST or None)
#         login_form = LoginForm(self.request.POST or None)
#         context = {'form':form,'login_form':login_form,'disp':False}

#         login_f = self.request.POST.get('login')
#         signup = self.request.POST.get('signup')
#         reset = self.request.POST.get('reset')
#         # print(self.request)
#         if login_f:
#             if login_form.is_valid():
#                 username = login_form.cleaned_data['username']
#                 password = login_form.cleaned_data['password']
#                 user = authenticate(self.request,username=username,password=password)
#                 if user is not None:
#                     login(self.request,user)
#                     if self.request.user.is_staff:
#                         return HttpResponseRedirect(reverse('admins'))
#                     else:
#                         return HttpResponseRedirect(reverse('dashboard'))
#                 else:
#                     print('user does not exist')
#                     context['errors'] = login_form.errors
#                     return render(self.request,self.template_name,context=context)
#             else: 
#                 context['errors'] = login_form.errors
#                 return render(self.request,self.template_name,context=context)

#         elif signup is not None:
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data['password1']
#                 email = form.cleaned_data['email']
#                 activation_key = get_activation_key()
#                 form.save()
#                 user = User.objects.get(username=username)
#                 customer = Customer.objects.get(user=user)
#                 customer.activation_key = activation_key
#                 customer.save()
#                 subject = 'Zeedah Account Verification'
#                 body = f'Hi {username} \n Please click on the link below to confirm your registration \n http://{settings.DOMAIN}/activate/{activation_key}'
#                 sender = 'zeedah@gmail.com'
#                 with mail.get_connection() as connection:
#                     mail.EmailMessage(
#                         subject, body, sender, [email],
#                         connection=connection,
#                     ).send()
#                 messages.success(self.request,'Kindly Check Your Email for link to activate your account')

#                 return self.get(*args,**kwargs)
#             else:
#                 context = {'form':form,'disp':True,'errors':form.errors}
#                 return render(self.request,self.template_name,context=context)

#         return render(self.request,self.template_name,context=context)
