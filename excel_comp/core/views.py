from django.shortcuts import render
from django.views import generic

class HomepageView(generic.View):
    template_name = 'core/landing_page.html'
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

class DashboardView(generic.View):
    template_name = 'core/dashboard.html'
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

