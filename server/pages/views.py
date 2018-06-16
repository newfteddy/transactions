import os
import sys
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
        change_chart()
        return HttpResponseRedirect('/main/')

    return HttpResponse("Failed")


def handle_uploaded_file(file):
    if not os.path.exists('../backend/tmp/'):
        os.mkdir('../backend/tmp/')

    with open('../backend/tmp/' + 'data.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    def post(self, request, **kwargs):
        return render(request, 'index.html', context=None)