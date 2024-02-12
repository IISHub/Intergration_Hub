import json
import requests

from datetime import datetime
from django.shortcuts import redirect, render

base_url = 'http://account-lookup-service-admin.local'

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
                response =  requests.get(url=endpoint, headers={'Content-Type': 'application/json;charset=utf-8', 'Accept': '*/*', 'Date': datetime.now().strftime('%d/%m/%Y')})
                oracle = response.json();

                oracle_list.extend(oracle)
        
            if oracle_id_type in oracles:
                oracles[oracle_id_type] = oracle_list

        context = {"oracle_id_types": oracle_id_types_list, "oracles": oracles}
        return render(request, "oracles.html", context) 