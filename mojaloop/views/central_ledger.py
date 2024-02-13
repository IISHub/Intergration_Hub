import json
import requests

from datetime import datetime
from django.shortcuts import redirect, render

from mojaloop.forms import CreateParticipantForm, HubAccountForm, InitialPositionAndLimitForm, LedgerAccountForm, ParticipantAccountForm, LimitForm, ParticipantEndpointForm, RecordTransactionForm, SettlementModelsForm

base_url = 'http://central-ledger.local'

headers={'Content-Type': 'application/json;charset=utf-8', 'Accept': '*/*', 'Date': datetime.now().strftime('%d/%m/%Y')}

def dashboard(request):
    endpoint = base_url + '/health'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers=headers)
        health = response.json();
        context = {"health": health}
        return render(request, "dashboard.html", context) 

def get_participants(request):
    endpoint = base_url + '/participants'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers=headers)
        participants = response.json();
        context = {"participants": participants}
        return render(request, "participants.html", context) 
    
def get_participants_limits(request):
    endpoint = base_url + '/participants/limits'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers=headers)
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
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(post_data))
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
        response =  requests.get(url=endpoint, headers=headers)
        participant = response.json();

        endpoint = base_url + '/participants/' + name + '/limits'
        response =  requests.get(url=endpoint, headers=headers)
        limits = response.json();

        endpoint = base_url + '/participants/' + name + '/endpoints'
        response =  requests.get(url=endpoint, headers=headers)
        endpoints = response.json();

        context = {"participant": participant, "limits": limits, "endpoints": endpoints}

        return render(request, "participant-view.html", context) 


def update_participant_activity(request, name, activity):
    endpoint = base_url + '/participants/' + name
    previous_page = request.META.get('HTTP_REFERER', None)

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers=headers, data=json.dumps(put_data))
        return redirect(previous_page)
    
def get_ledger_account_types(request):
    endpoint = base_url + '/ledgerAccountTypes'

    if request.method == 'GET':
        response =  requests.get(url=endpoint, headers=headers)
        ledgeraccounts = response.json();
        context = {"ledgeraccounts": ledgeraccounts}
        return render(request, "ledgeraccounts.html", context) 

def add_ledger_account_type(request):
    endpoint = base_url + '/ledgerAccountTypes'

    if request.method == 'POST':
        form = LedgerAccountForm(request.POST)
        if form.is_valid():
            post_data = {
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "isActive": form.cleaned_data["active"],
                "isSettleable": form.cleaned_data["settleable"],
            }
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(post_data))
            if response.status_code == 200:
                return redirect('ledgeraccounts')
            else:
                json_response = response.json();
                context = {"form":form, "form_type":"Create", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "ledgeraccount-form.html", context)
        else:
            context = {"form":form, "form_type":"Create", "error": "Something went wrong while processing the form"}
            return render(request, "ledgeraccount-form.html", context)
    else:
        form = LedgerAccountForm()
        context = {"form":form, "form_type":"Create"}
        return render(request, "ledgeraccount-form.html", context)
    
def add_participant_account(request, name):
    endpoint = base_url + '/participants/' + name + '/accounts'

    if request.method == 'POST':
        if name == 'Hub': form = HubAccountForm(request.POST)
        else: form = ParticipantAccountForm(request.POST)

        if form.is_valid():
            put_data = {
                "currency": form.cleaned_data['currency'],
                "type": form.cleaned_data['type'],
            }
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                if name == 'Hub': form = HubAccountForm(initial=request.POST)
                else: form = ParticipantAccountForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-account-form.html", context)
    else:
        if name == 'Hub': form = HubAccountForm()
        else: form = ParticipantAccountForm()
        context = {"form": form, "participant_name": name, "form_type":"Add"}
        return render(request, "participant-account-form.html", context)
    
def update_participant_account_activity(request, name, id, activity):
    endpoint = base_url + '/participants/' + name + '/accounts/' + str(id)
    previous_page = request.META.get('HTTP_REFERER', None)

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers=headers, data=json.dumps(put_data))
        return redirect(previous_page)
    
def record_participant_transfer(request, name, id):
    endpoint = base_url + '/participants/' + name + '/accounts/' + str(id) 

    if request.method == 'POST':
        form = RecordTransactionForm(request.POST)

        if form.is_valid():
            post_data = {
                "transferID": form.cleaned_data['transfer_id'],
                "externalReferences": form.cleaned_data['external_reference'],
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

            response = requests.post(url=endpoint, headers=headers, data=json.dumps(post_data))
            if response.status_code == 202:
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
    endpoint = base_url + '/participants/' + name + '/initialPositionAndLimits'
        
    if request.method == 'POST':
        form = InitialPositionAndLimitForm(request.POST)

        if form.is_valid():
            put_data = {
                "currency": form.cleaned_data['currency'],
                "limit": {
                    "type": form.cleaned_data['limit_type'],
                    "value": form.cleaned_data['limit_value']
                },
                "initialPosition": form.cleaned_data['initial_position']
            }
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(put_data))
            if response.status_code == 201:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = InitialPositionAndLimitForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Add", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-limit-form.html", context)
    else:
        form = InitialPositionAndLimitForm()
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
            response = requests.put(url=endpoint, headers=headers, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                form = LimitForm(initial=request.POST)
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-limit-form.html", context)
    else:
        response =  requests.get(url=endpoint, headers=headers)
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
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(put_data))
            if response.status_code == 201:
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
            response = requests.put(url=endpoint, headers=headers, data=json.dumps(put_data))
            if response.status_code == 200:
                return redirect('get-participant', name=name)
            else:
                json_response = response.json();
                context = {"form":form, "participant_name":name, "account":id, "form_type":"Record", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "participant-endpoint-form.html", context)
    else:
        response =  requests.get(url=endpoint, headers=headers)
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
        response =  requests.get(url=endpoint, headers=headers)
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
                "settlementInterchange": form.cleaned_data["settlementInterchange"],
                "settlementDelay": form.cleaned_data["settlementDelay"],
                "requireLiquidityCheck": form.cleaned_data["requireLiquidityCheck"],
                "ledgerAccountType": form.cleaned_data["ledgerAccountType"],
                "autoPositionReset": form.cleaned_data["autoPositionReset"],
                "currency": form.cleaned_data["currency"],
                "settlementAccountType": form.cleaned_data["settlementAccountType"],
            }

            response = requests.post(url=endpoint, headers=headers, data=json.dumps(post_data))
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
        response =  requests.get(url=endpoint, headers=headers)
        settlementmodel = response.json();
        context = {"settlementmodel": settlementmodel}
        return render(request, "settlement-model-view.html", context) 

            
def update_settlement_model_activity(request, name, activity):
    endpoint = base_url + '/settlementModels/' + name
    previous_page = request.META.get('HTTP_REFERER', None)

    if request.method == 'GET':
        put_data = {"isActive": activity}
        requests.put(url=endpoint, headers=headers, data=json.dumps(put_data))
        return redirect(previous_page)
    
