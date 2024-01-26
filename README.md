# Mojaloops Integration Example

This document outlines an example integration with the payment manager

## Parties Endpoint

### Endpoint:
http://34.132.18.46:8000/mojaloops/parties/

### Payload:
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

### Response
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
http://34.132.18.46:8000/mojaloops/quotes/

### Payload:
```json
{
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123",
    "accept_receiver": true
}
```

### Response
```json
{
    "amount": "100",
    "fsp_fee": "0.5",
    "fsp_commision": "0.2",
    "receiving_amount": "99.7",
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123"
}
```

## Transfer Endpoint

### Endpoint:
http://34.132.18.46:8000/mojaloops/transfer/

### Payload:
```json
{
    "transfer_id": "850cbb1e-18d4-492c-86ce-dfa547d0f123",
    "accept_charges": true
}
```

### Response
```json
{
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