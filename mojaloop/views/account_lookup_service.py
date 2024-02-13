import json
import requests

from datetime import datetime
from django.shortcuts import redirect, render

from mojaloop.forms import OracleForm

base_url = 'http://account-lookup-service-admin.local'

headers={'Content-Type': 'application/json;charset=utf-8', 'Accept': '*/*', 'Date': datetime.now().strftime('%d/%m/%Y')}

oracle_id_types_list = ["MSISDN", "EMAIL", "PERSONAL_ID", "BUSINESS", "DEVICE", "ACCOUNT_ID", "IBAN", "ALIAS"]

currency_list = ["INR", "USD", "ZMW"]

def get_oracles(request):
    if request.method == 'GET':
        oracles = {
            "MSISDN": [],
            "EMAIL": [],
            "PERSONAL_ID": [],
            "BUSINESS": [],
            "DEVICE": [],
            "ACCOUNT_ID": [],
            "IBAN": [],
            "ALIAS": [],
        }
        
        for oracle_id_type in oracle_id_types_list:
            oracle_list = []

            for currency in currency_list:
                endpoint = base_url + '/oracles?currency=' + currency + '&type=' + oracle_id_type
                response =  requests.get(url=endpoint, headers=headers)
                oracle = response.json();

                oracle_list.extend(oracle)
        
            if oracle_id_type in oracles:
                oracles[oracle_id_type] = oracle_list

        context = {"oracle_id_types": oracle_id_types_list, "oracles": oracles}
        return render(request, "oracles.html", context)
    
def create_oracle(request):
    endpoint = base_url + '/oracles'

    if request.method == 'POST':
        form = OracleForm(request.POST)

        if form.is_valid():
            post_data = {
                "oracleIdType": form.cleaned_data['oracle_id_type'],
                "endpoint": {
                    "value": "http://moja-simulator.local/oracle",
                    "endpointType": "URL"
                },
                "currency": form.cleaned_data['currency'],
                "isDefault": 1
            }
            response = requests.post(url=endpoint, headers=headers, data=json.dumps(post_data))
            if response.status_code == 201:
                return redirect('oracles')
            else:
                json_response = response.json();
                form = OracleForm(initial=request.POST)
                context = {"form":form, "form_type":"Create", "error": json_response.get("errorInformation", {}).get("errorDescription")}
                return render(request, "oracle-form.html", context)
        else:
            context = {"form":form, "form_type":"Create", "error": "Something when wrong while processing the form"}
            return render(request, "oracle-form.html", context)
    else:
        form = OracleForm()
        context = {"form": form, "form_type":"Create"}
        return render(request, "oracle-form.html", context)

def update_oracle(request, oracle_id_type, oracle_id):
    pass

def delete_oracle(request, oracle_id):
    endpoint = base_url + '/oracles/' + str(oracle_id)

    if request.method == 'GET':
        response =  requests.delete(url=endpoint, headers=headers)
        return redirect('oracles')
