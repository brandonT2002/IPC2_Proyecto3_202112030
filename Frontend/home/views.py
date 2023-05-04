from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Archivo
import requests as req
import json

# Create your views here.
def home(requests):
    path1 = ''
    path2 = ''
    if requests.method == 'POST' and 'upProfiles' in requests.POST and requests.FILES['file1']:
        try:
            print('ENTRAAAAAAAA')
            file1 = requests.FILES['file1']
            fs = FileSystemStorage()
            filename = fs.save(file1.name, file1)
            uploaded_file_url = fs.url(filename)
            
            return render(requests, 'home/index.html', {
                'uploaded_file_url': uploaded_file_url,'status':'working','path1':'asdf','path2':'asdf'
            })
        except: print('ATRAPA ERROR')
    if requests.method == 'POST' and 'upMessages' in requests.POST:
        print('upMessages')
    return render(requests,'home/index.html',{'status':'working','path1':path1,'path2':path2,'uploaded_file_url':''})

def upload(requests):
    print('ENTRAAAAAAAA')
    if requests.method == 'POST' and requests.FILES['file1']:
        print('Entra aqui')
        file1 = requests.FILES['file1']
        fs = FileSystemStorage()
        filename = fs.save(file1.name, file1)
        uploaded_file_url = fs.url(filename)
        print('RUTA ->',uploaded_file_url)
        return render(requests, 'home/index.html', {
            'uploaded_file_url': uploaded_file_url,'status':'working','path1':'asdf','path2':'asdf'
        })
    return render(requests,'home/index.html',{'status':'working','path1':'asdf','path2':'asdf'})