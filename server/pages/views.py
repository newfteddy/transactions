import os
import sys
import pandas as pd
import pickle
sys.path.append('../backend/code')

from transform import change_chart
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, 'index.html', {'what':'DWT File Upload with Django'})


def upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['myfile'])
        if check():
            change_chart()
            return HttpResponseRedirect('/main/')
        else:
            return HttpResponse("Bad input file")
    return HttpResponse("Failed")


def check():
    df = pd.read_csv('../backend/tmp/data.csv')
    if len(df.columns) != 2:
        return False
    if df.shape[0] < 10:
        return False
    if df[df[df.columns[1]] != 0].shape[0] < 3:
        return False
    codes = pickle.load(open('./pages/mcc.pkl', 'rb'))
    for x in df[df.columns[0]]:
        if x not in codes:
            return False
    return True


def handle_uploaded_file(file):
    if not os.path.exists('../backend/tmp/'):
        os.mkdir('../backend/tmp/')

    with open('../backend/tmp/' + 'data.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return destination



class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    def post(self, request, **kwargs):
        return render(request, 'index.html', context=None)