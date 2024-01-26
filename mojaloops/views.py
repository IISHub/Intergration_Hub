import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import requests
import uuid

def generate_uuid():
    return str(uuid.uuid4())

@csrf_exempt
@api_view(['GET','POST'])
def send_money(request):
    if request.method == 'GET':
        return JsonResponse({"http://localhost:3003/sendmoney": "The HTTP request POST /sendmoney is used by the Payer DFSP to request the movement of funds from the Payer DFSP to the Payee DFSP."}, status=200)
    if request.method == 'POST':
        try:
            # Get the request body
            request_body = request.body.decode('utf-8')

            # Specify the URL
            url = "http://localhost:3003/sendmoney"

            # Make the POST request
            response = requests.post(url=url, data=request_body, headers={"Content-Type": "application/json;charset=utf-8"})

            json_response = response.json();

            # Return the response as JsonResponse
            return JsonResponse(json_response, status=response.status_code)
        except Exception as e:
            # Handle exceptions if any
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
@api_view(['GET','POST'])
def get_party(request):
    if request.method == 'GET':
        return JsonResponse({"http://localhost:4001/transfers": "The HTTP request POST /transfers is sent to the Payee DFSP, and it is used to request the creation of a transfer for the transfer party."}, status=200)
    if request.method == 'POST':
        try:
            post_data = {
                "from": {
                    "displayName": request.data.get('sender_name'),
                    "idType": request.data.get('sender_id_type'),
                    "idValue": request.data.get('sender_id_value'),
                },
                "to": {
                    "idType": request.data.get('receiver_id_type'),
                    "idValue": request.data.get('receiver_id_value'),
                },
                "amountType": "SEND",
                "transactionType": "TRANSFER",
                "note": request.data.get('note'),
                "currency": request.data.get('currency'),
                "amount": request.data.get('amount'),
                "homeTransactionId": generate_uuid()
            }

            url = "http://localhost:4001/transfers"

            response = requests.post(url=url, data=json.dumps(post_data), headers={"Content-Type": "application/json;charset=utf-8"})

            json_response = response.json();
            extracted_data = {
                "first_name": json_response.get("to", {}).get("firstName"),
                "middle_name": json_response.get("to", {}).get("middleName"),
                "last_name": json_response.get("to", {}).get("lastName"),
                "fsp_id": json_response.get("to", {}).get("fspId"),
                "account_id": json_response.get("to", {}).get("idValue"),
                "currency": json_response.get("currency"),
                "amount": json_response.get("amount"),
                "transfer_id": json_response.get("transferId")
            }

            return JsonResponse(extracted_data, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
@api_view(['GET','POST'])
def get_quote(request):
    if request.method == 'GET':
        return JsonResponse({"http://localhost:4001/transfers/TRANSFER_ID": "The HTTP request PUT /transfers/TRANSFER_ID is sent to the Payee DFSP, and it is used to notify the Payee DFSP about the final state of a transfer, to indicate whether the transfer has been committed or aborted in the Switch."}, status=200)
    if request.method == 'POST':
        try:
            transferId = request.data.get('transfer_id')

            data = {"acceptParty": request.data.get('accept_receiver')}

            url = f"http://localhost:4001/transfers/{transferId}"

            response = requests.put(url=url, data=json.dumps(data), headers={"Content-Type": "application/json;charset=utf-8"})

            json_response = response.json();
            extracted_data = {
                "amount": json_response.get("quoteResponse", {}).get("body", {}).get("transferAmount", {}).get("amount"),
                "fsp_fee": json_response.get("quoteResponse", {}).get("body", {}).get("payeeFspFee", {}).get("amount"),
                "fsp_commision": json_response.get("quoteResponse", {}).get("body", {}).get("payeeFspCommission", {}).get("amount"),
                "receiving_amount": json_response.get("quoteResponse", {}).get("body", {}).get("payeeReceiveAmount", {}).get("amount"),
                "transfer_id": json_response.get("transferId")
            }

            return JsonResponse(extracted_data, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
@api_view(['GET','POST'])
def accept_or_decline_transfer(request):
    if request.method == 'GET':
        return JsonResponse({"http://localhost:4001/transfers/TRANSFER_ID": "The HTTP request PUT /transfers/TRANSFER_ID is sent to the Payee DFSP, and it is used to notify the Payee DFSP about the final state of a transfer, to indicate whether the transfer has been committed or aborted in the Switch."}, status=200)
    if request.method == 'POST':
        try:
            transferId = request.data.get('transfer_id')

            data = {"acceptQuote": request.data.get('accept_charges')}

            url = f"http://localhost:4001/transfers/{transferId}"

            response = requests.put(url=url, data=json.dumps(data), headers={"Content-Type": "application/json;charset=utf-8"})

            json_response = response.json();
            extracted_data = {
                "sender_account_id": json_response.get("from", {}).get("idValue"),
                "receiver_first_name": json_response.get("to", {}).get("firstName"),
                "receiver_middle_name": json_response.get("to", {}).get("middleName"),
                "receiver_last_name": json_response.get("to", {}).get("lastName"),
                "receiver_fsp_id": json_response.get("to", {}).get("fspId"),
                "receiver_account_id": json_response.get("to", {}).get("idValue"),
                "currency": json_response.get("currency"),
                "amount": json_response.get("amount"),
                "fsp_fee": json_response.get("quoteResponse", {}).get("body", {}).get("payeeFspFee", {}).get("amount"),
                "fsp_commision": json_response.get("quoteResponse", {}).get("body", {}).get("payeeFspCommission", {}).get("amount"),
                "receiving_amount": json_response.get("quoteResponse", {}).get("body", {}).get("payeeReceiveAmount", {}).get("amount"),
                "transfer_id": json_response.get("transferId")
            }

            return JsonResponse(extracted_data, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)