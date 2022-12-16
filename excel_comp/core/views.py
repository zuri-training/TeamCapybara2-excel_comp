from io import BytesIO
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from core.mixins import CheckVerificationMixin

import pandas as pd
import json
import os
import xlsxwriter
from openpyxl import Workbook
from openpyxl.styles import Font, Color, colors, fills
from openpyxl.utils.dataframe import dataframe_to_rows

def highlight_duplicate(dataframe,duplicates):
    wb = Workbook()
    ws = wb.active

    for row_index in duplicates:
        row = ws.row_dimensions[row_index]
        row.fill = fills.PatternFill(patternType='solid', fgColor=Color(rgb='00FF00'))

    wb.save("pandas_openpyxl.xlsx")
    return wb



def generate(x,params=[]):
    array_len = list(range(len(x)))        
    v = {}
    
    for i,element in enumerate(x):    
        v[i] = {
            'cells':{ }
        }

    for i in array_len:
        for k,item in enumerate(x[i]):
            v[i]['cells'][k] = { 'text': item}

    if len(params) > 0:
        for item in params:
            for x in v[item]['cells']:
                v[item]['cells'][x]['style'] = 1
    return v


class HomepageView(generic.View):
    template_name = 'core/landing_page.html'
    
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

class DashboardView(generic.View):
    template_name = 'core/dashboard.html'
    redirect_url = reverse_lazy('confirm')

    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        file = request.FILES['excel_file']
        if file:
            dat = pd.read_excel(file)
            data = pd.DataFrame(dat)

            dup_data = data[data.duplicated(keep=False)]
            duplicates_list = dup_data.index.tolist()
            dup_data = dup_data.values.tolist()
            result = generate(dup_data,[])
            result = json.dumps(result,cls=PdEncoder)

            datas = data.values.tolist()
            da = generate(datas,duplicates_list)
            da = json.dumps(da,cls=PdEncoder)

            original = data.values.tolist()
            original = generate(original,[])
            final = json.dumps(original,cls=PdEncoder)

            file_size = file.seek(0,os.SEEK_END)
            file.seek(0,os.SEEK_SET)

            highlighted_duplicates = highlight_duplicate(data,duplicates_list)

            context = {'result':da,'duplicates':final,'data':dat.to_json(),'total_duplicates':len(dup_data),
                        'size':file_size/1000,'original':json.dumps(datas,cls=PdEncoder),
                        'highlighted':highlighted_duplicates
                    }

            return render(request,'core/results.html',context)
            
        return render(request,self.template_name)




class ProfileView(LoginRequiredMixin,CheckVerificationMixin,generic.View):
    template_name = 'core/profile.html'
    redirect_url = reverse_lazy('confirm')
    def get(self,request):

        return render(request,self.template_name)

class AboutView(generic.View):
    template_name = 'core/about.html'
    def get(self,request):

        return render(request,self.template_name)

class SupportView(generic.View):
    template_name = 'core/support.html'
    def get(self,request):

        return render(request,self.template_name)

class CookiesView(generic.View):
    template_name = 'core/cookies.html'
    def get(self,request):

        return render(request,self.template_name)

class PrivacyView(generic.View):
    template_name = 'core/privacy.html'
    def get(self,request):

        return render(request,self.template_name)

class HowToUseView(generic.View):
    template_name = 'core/how_to_use.html'
    def get(self,request):

        return render(request,self.template_name)

class PdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp ):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
