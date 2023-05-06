from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Archivo
import requests as req
import json

# Create your views here.
def home(requests):
    profiles = json.loads(req.get('http://127.0.0.1:4000/profiles').text)
    messages = json.loads(req.get('http://127.0.0.1:4000/messages').text)
    dates = json.loads(req.get('http://127.0.0.1:4000/getDates').text)
    users = json.loads(req.get('http://127.0.0.1:4000/getUsers').text)
    if requests.method == 'POST' and 'upProfiles' in requests.POST and requests.FILES['file1']:
        try:
            file1 = requests.FILES['file1']
            fs = FileSystemStorage()
            filename = fs.save(file1.name, file1)
            req.post('http://127.0.0.1:4000/profiles',json = {'filename':filename})
            profiles = json.loads(req.get('http://127.0.0.1:4000/profiles').text)
        except: pass
    elif requests.method == 'POST' and 'upMessages' in requests.POST and requests.FILES['file2']:
        try:
            file2 = requests.FILES['file2']
            fs = FileSystemStorage()
            filename = fs.save(file2.name, file2)
            req.post('http://127.0.0.1:4000/messages',json = {'filename':filename})
            messages = json.loads(req.get('http://127.0.0.1:4000/messages').text)
            dates = json.loads(req.get('http://127.0.0.1:4000/getDates').text)
            users = json.loads(req.get('http://127.0.0.1:4000/getUsers').text)
        except: pass
    elif requests.method == 'POST' and 'upMessage' in requests.POST and requests.FILES['file3']:
        try:
            file3 = requests.FILES['file3']
            fs = FileSystemStorage()
            filename = fs.save(file3.name, file3)
            # `request3` is sending a POST request to the URL `http://127.0.0.1:4000/request3` with a
            # JSON payload containing the filename of a file uploaded by the user. The response from
            # the server is then stored in the `request3` variable as a JSON object. The contents of
            # this variable are then displayed on the webpage as part of the rendered template.
            request3 = json.loads(req.post('http://127.0.0.1:4000/request3',json = {'filename':filename}).text)
            return render(
                requests,
                'home/index.html',
                {
                    'status':'working',
                    'inputP':f'Input:\n\n{profiles.get("inputP")}','outputP':f'Output:\n\n{profiles.get("outputP")}',
                    'inputM':f'Input:\n\n{messages.get("inputM")}','outputM':f'Output:\n\n{messages.get("outputM")}',
                    'inputR3':f'Input:\n\n{request3.get("inputR3")}','outputR3':f'Output:\n\n{request3.get("outputR3")}',
                    'dates':dates.get("dates"),
                    'users':users.get("users")
                }
            )
        except: pass
    elif requests.method == 'POST' and 'details' in requests.POST:
        selectedDate = requests.POST['selectDate1']
        selectedUser = requests.POST['selectUser1']
        if selectedUser == 'Todos los Usuarios':
            selectedUser = 'NONE'
            request1 = json.loads(req.post('http://127.0.0.1:4000/request1',json = {'date': selectedDate,'user':selectedUser}).text)
            print(request1)
            return render(
                requests,
                'home/index.html',
                {
                    'status':'working',
                    'inputP':f'Input:\n\n{profiles.get("inputP")}','outputP':f'Output:\n\n{profiles.get("outputP")}',
                    'inputM':f'Input:\n\n{messages.get("inputM")}','outputM':f'Output:\n\n{messages.get("outputM")}',
                    'outputR1':request1.get("response")
                }
            )
    # return render(requests, 'home/index.html', {'status':'working','inputP':f'Input:\n\n{peticion.get("inputP")}','outputP':f'Output:\n\n{peticion.get("outputP")}'})
    # return render(requests, 'home/index.html', {'status':'working','inputM':f'Input:\n\n{peticion.get("inputM")}','outputM':f'Output:\n\n{peticion.get("outputM")}'})
    # return render(requests, 'home/index.html', {'status':'working','inputR3':f'Input:\n\n{peticion.get("inputR3")}','outputR3':f'Output:\n\n{peticion.get("outputR3")}'})
    return render(
        requests,
        'home/index.html',
        {
            'status':'working',
            'inputP':f'Input:\n\n{profiles.get("inputP")}','outputP':f'Output:\n\n{profiles.get("outputP")}',
            'inputM':f'Input:\n\n{messages.get("inputM")}','outputM':f'Output:\n\n{messages.get("outputM")}',
            'dates':dates.get("dates"),
            'users':users.get("users")
        }
    )