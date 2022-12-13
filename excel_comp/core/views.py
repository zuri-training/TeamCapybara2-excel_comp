from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from core.mixins import CheckVerificationMixin

class HomepageView(generic.View):
    template_name = 'core/landing_page.html'
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

class DashboardView(LoginRequiredMixin,CheckVerificationMixin,generic.View):
    template_name = 'core/dashboard.html'
    redirect_url = reverse_lazy('login')
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

