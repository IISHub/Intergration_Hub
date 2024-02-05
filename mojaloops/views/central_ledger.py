import json
import requests

from django.shortcuts import redirect, render

from mojaloops.forms import CreateParticipantForm, HubAccountForm, LimitForm, ParticipantEndpointForm, RecordTransactionForm, SettlementModelsForm

base_url = 'http://central-ledger.local'

def dashboard(request):
    endpoint = base_url + '/health'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        health = response.json();
        context = {"health": health}
        return render(request, "dashboard.html", context) 

def get_participants(request):
    endpoint = base_url + '/participants'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        participants = response.json();
        context = {"participants": participants}
        return render(request, "participants.html", context) 
    
def get_participants_limits(request):
    endpoint = base_url + '/participants/limits'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        participants = response.json();
        context = {"participants": participants}
        return render(request, "participant-limits.html", context) 


def create_participant(request):
    endpoint = base_url + '/participants'

    if request.method == 'POST':
        form = CreateParticipantForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            currency = form.cleaned_data['currency']
            post_data = {"name": name, "currency": currency}
            response = requests.post(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(post_data))
            if response.status_code == 201:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = CreateParticipantForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-form.html", context)
        else:
            return render(request, "participant-form.html", context)
    else:
        form = CreateParticipantForm()
        context = {"form": form}
        return render(request, "participant-form.html", context)

def view_participant(request, name):
    if request.method == 'GET':
        endpoint = base_url + '/participants/' + name
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        participant = response.json();

        endpoint = base_url + '/participants/' + name + '/limits'
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        limits = response.json();

        endpoint = base_url + '/participants/' + name + '/endpoints'
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        endpoints = response.json();

        context = {"participant": participant, "limits": limits, "endpoints": endpoints}

        return render(request, "participant-view.html", context) 


def update_participant_activity(request, name, activity):
    endpoint = base_url + '/participants/' + name

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
        return redirect('get-participant', name=name)
    
def add_participant_account(request, name):
    endpoint = base_url + '/participants/' + name + '/accounts'

    if request.method == 'POST':
        form = HubAccountForm(request.POST)

        if form.is_valid():
            put_data = {
                "currency": form.cleaned_data['currency'],
                "type": form.cleaned_data['type'],
            }
            response = requests.post(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = HubAccountForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-account-form.html", context)
    else:
        form = HubAccountForm()
        context = {"form": form, "participant_name": name, "form_type":"Add"}
        return render(request, "participant-account-form.html", context)
    
def update_participant_account_activity(request, name, id, activity):
    endpoint = base_url + '/participants/' + name + '/accounts/' + str(id) 

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
        return redirect('get-participant', name=name)
    
def record_participant_transfer(request, name, id):
    endpoint = base_url + '/participants/' + name + '/accounts/' + str(id) 

    if request.method == 'POST':
        form = RecordTransactionForm(request.POST)

        if form.is_valid():
            post_data = {
                "transferID": form.cleaned_data['transfer_id'],
                "externalReferences": form.cleaned_data['external_references'],
                "action": form.cleaned_data['action'],
                "reason": form.cleaned_data['reason'],
                "amount": {
                    "amount": form.cleaned_data['amount'],
                    "currency": form.cleaned_data['currency'],
                },
                "extensionList": {
                    "extension": [
                        {
                            "key": "scheme",
                            "value": "abc"
                        }
                    ]
                }
            }

            response = requests.post(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(post_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = RecordTransactionForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-transfer-record-form.html", context)
    else:
        form = RecordTransactionForm()
        context = {"form":form, "participant_name":name, "account":id, "form_type":"Record"}
        return render(request, "participant-transfer-record-form.html", context)
        
def add_participant_limit(request, name):
    endpoint = base_url + '/participants/' + name + '/limits'

    if request.method == 'POST':
        form = LimitForm(request.POST)

        if form.is_valid():
            put_data = {
                "currency": form.cleaned_data['currency'],
                "limit": {
                    "type": form.cleaned_data['limit_type'],
                    "value": form.cleaned_data['limit_value'],
                    "alarmPercentage": form.cleaned_data['alarm_percentage']
                }
            }
            response = requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = LimitForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-limit-form.html", context)
    else:
        form = LimitForm()
        context = {"form": form, "participant_name": name, "form_type":"Add"}
        return render(request, "participant-limit-form.html", context)
    
def update_participant_limit(request, name, limit_type):
    endpoint = base_url + '/participants/' + name + '/limits'

    if request.method == 'POST':
        form = LimitForm(request.POST)

        if form.is_valid():
            put_data = {
                "currency": form.cleaned_data['currency'],
                "limit": {
                    "type": form.cleaned_data['limit_type'],
                    "value": form.cleaned_data['limit_value'],
                    "alarmPercentage": form.cleaned_data['alarm_percentage']
                }
            }
            response = requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = LimitForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-limit-form.html", context)
    else:
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        limits = response.json();
        for participant_limit in limits:
            if participant_limit.get('limit', {}).get('type') == limit_type:
                initial_data = {
                    "current": participant_limit.get('currency'),
                    "limit_type": participant_limit.get('limit', {}).get('type'),
                    "limit_value": participant_limit.get('limit', {}).get('value'),
                    "alarm_percentage": participant_limit.get('limit', {}).get('alarmPercentage')
                }
        
        form = LimitForm(initial=initial_data)
        context = {"form": form, "participant_name": name, "limit": limit_type, "form_type":"Update"}
        return render(request, "participant-limit-form.html", context)

def add_participant_endpoint(request, name):
    endpoint = base_url + '/participants/' + name + '/endpoints'

    if request.method == 'POST':
        form = ParticipantEndpointForm(request.POST)

        if form.is_valid():
            put_data = {
                "type": form.cleaned_data['type'],
                "value": form.cleaned_data['value'],
            }
            response = requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-endpoint-form.html", context)
    else:
        form = ParticipantEndpointForm()
        context = {"form": form, "participant_name": name, "form_type":"Add"}
        return render(request, "participant-endpoint-form.html", context)
    
def update_participant_endpoint(request, name, endpoint_type):
    endpoint = base_url + '/participants/' + name + '/endpoints'

    if request.method == 'POST':
        form = ParticipantEndpointForm(request.POST)

        if form.is_valid():
            put_data = {
                "type": form.cleaned_data['type'],
                "value": form.cleaned_data['value'],
            }
            response = requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-endpoint-form.html", context)
    else:
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        endpoints = response.json();
        for endpoint in endpoints:
            if endpoint.get('type') == endpoint_type:
                initial_data = {
                    "type": endpoint.get('type'),
                    "value": endpoint.get('value'),
                }
        
        form = ParticipantEndpointForm(initial=initial_data)
        context = {"form": form, "participant_name": name, "endpoint_type": endpoint_type, "form_type":"Update"}
        return render(request, "participant-endpoint-form.html", context)

def get_settlement_models(request):
    endpoint = base_url + '/settlementModels'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        settlementmodels = response.json();
        context = {"settlementmodels": settlementmodels}
        return render(request, "settlement-models.html", context)     

def create_settlement_model(request):
    endpoint = base_url + '/settlementModels'

    if request.method == 'POST':
        form = SettlementModelsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            
            post_data = {
                "name": form.cleaned_data["name"],
                "settlementGranularity": form.cleaned_data["settlementGranularity"],
                "settlementIntercharge": form.cleaned_data["settlementIntercharge"],
                "settlementDelay": form.cleaned_data["settlementDelay"],
                "requiredLiquidityCheck": form.cleaned_data["requiredLiquidityCheck"],
                "ledgerAccountType": form.cleaned_data["ledgerAccountType"],
                "autoPositionReset": form.cleaned_data["autoPositionReset"],
                "settlementAccountType": form.cleaned_data["settlementAccountType"],
            }

            response = requests.post(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(post_data))
            if response.status_code == 201:
                return redirect('get-settlement-model', name=name)
            else:
                json_response = response.json();
                form = SettlementModelsForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "settlement-model-form.html", context)
    else:
        form = SettlementModelsForm()
        context = {"form": form}
        return render(request, "settlement-model-form.html", context)
            
def view_settlement_model(request, name):
    endpoint = base_url + '/settlementModels/' + name

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'})
        settlementmodel = response.json();
        context = {"settlementmodel": settlementmodel}
        return render(request, "settlement-model-view.html", context) 

            
def update_settlement_model_activity(request, name, activity):
    endpoint = base_url + '/settlementModels/' + name

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8'}, data=json.dumps(put_data))
        return redirect('get-settlement-model', name=name)