# mojaloop Integration Example

This document outlines an example integration with the payment manager

## Parties Endpoint

### Endpoint:
http://104.197.56.193:8000/mojaloop/parties/

Retrieves receiver information

### Sample Payload:
```json
{
    "sender_name":"Firstname Lastname",
    "sender_id_type":"MSISDN",
    "sender_id_value": "22507008181",
    "receiver_id_type":"MSISDN",
    "receiver_id_value": "22556999125",
    "currency": "USD",
    "amount": "100",
    "note": "test payment"
}
```

### Sample Response (success)
```json
{
    "first_name": "Chris",
    "middle_name": "N",
    "last_name": "Gonzalez",
    "fsp_id": "testingtoolkitdfsp",
    "account_id": "22556999125",
    "currency": "USD",
    "amount": "100",
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123"
}
```

## Quotes Endpoint

### Endpoint:
http://104.197.56.193:8000/mojaloop/quotes/

Retrievies transaction charges

### Sample Payload:
```json
{
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123",
    "accept_receiver": true
}
```

### Sample Response (success)
```json
{
    "amount": "100",
    "fsp_fee": "0.5",
    "fsp_commision": "0.2",
    "receiving_amount": "99.7",
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123"
}
```

### Sample Response (alternative response)
If the ```accept_receiver``` is ```false``` or the reciever information was rejected.
```json
{
    "transfer_state": "ABORTED"
}
```

## Transfer Endpoint

### Endpoint:
http://104.197.56.193:8000/mojaloop/transfer/

Sends transfer confirmation

### Sample Payload:
```json
{
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123",
    "accept_charges": true
}
```

### Sample Response (success)
```json
{
    "sender_name":"Firstname Lastname",
    "sender_account_id": "22507008181",
    "receiver_first_name": "Chris",
    "receiver_middle_name": "N",
    "receiver_last_name": "Gonzalez",
    "receiver_fsp_id": "testingtoolkitdfsp",
    "receiver_account_id": "22556999125",
    "currency": "USD",
    "amount": "100",
    "fsp_fee": "0.5",
    "fsp_commision": "0.2",
    "receiving_amount": "99.7",
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123"
}
```

### Sample Response (alternative response)
If the ```accept_charges``` is ```false``` or the transaction charges were rejected.
```json
{
    "transfer_state": "ABORTED"
}
```
