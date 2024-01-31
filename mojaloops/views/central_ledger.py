import json
import requests

from django.shortcuts import redirect, render

from mojaloops.forms import CreateParticipantForm

base_url = 'http://central-ledger.local'

def get_participants(request):
    endpoint = base_url + '/participants'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        participants = response.json();
        context = {"participants": participants}
        return render(request, "dashboard.html", context) 

def create_participant(request):
    endpoint = base_url + '/participants'
    form = CreateParticipantForm()
    context = {"form": form}
    if request.method == 'POST':
        form = CreateParticipantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            currency = form.cleaned_data['currency']
            post_data = {"name": name, "currency": currency}
            response = requests.post(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(post_data))
            if response.status_code == 201:
                return redirect(f'/participants/{name}')
            else:
                return render(request, "participants-create.html", context)
        else:
            return render(request, "participants-create.html", context)
    else:
        return render(request, "participants-create.html", context)
    
def view_participant(request, name):
    endpoint = base_url + '/participants/' + name
    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        participant = response.json();
        context = {"participant": participant}
        return render(request, "participant-view.html", context) 