from django import forms

# currency_field_list = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS", "SPL", "SRD", "STD", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VEF", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "XTS", "YER", "ZAR", "ZMW", "ZWD"]

currency_field_list = ["USD", "ZMW"]

paired_currencies = [(currency, currency) for currency in currency_field_list]


enpoint_types_field_list = ["FSPIOP_CALLBACK_URL_PARTICIPANT_SUB_ID_PUT", "FSPIOP_CALLBACK_URL_PARTICIPANT_SUB_ID_PUT_ERROR", "FSPIOP_CALLBACK_URL_PARTICIPANT_SUB_ID_DELETE", "FSPIOP_CALLBACK_URL_PARTIES_SUB_ID_GET", "FSPIOP_CALLBACK_URL_PARTIES_SUB_ID_PUT", "FSPIOP_CALLBACK_URL_PARTIES_SUB_ID_PUT_ERROR", "FSPIOP_CALLBACK_URL_AUTHORIZATIONS", "FSPIOP_CALLBACK_URL_PARTICIPANT_PUT", "FSPIOP_CALLBACK_URL_PARTICIPANT_PUT_ERROR", "FSPIOP_CALLBACK_URL_PARTICIPANT_BATCH_PUT", "FSPIOP_CALLBACK_URL_PARTICIPANT_BATCH_PUT_ERROR", "FSPIOP_CALLBACK_URL_PARTIES_GET", "FSPIOP_CALLBACK_URL_PARTIES_PUT", "FSPIOP_CALLBACK_URL_PARTIES_PUT_ERROR", "FSPIOP_CALLBACK_URL_QUOTES", "FSPIOP_CALLBACK_URL_TRX_REQ_SERVICE", "FSPIOP_CALLBACK_URL_TRANSFER_POST", "FSPIOP_CALLBACK_URL_TRANSFER_PUT", "FSPIOP_CALLBACK_URL_TRANSFER_ERROR", "FSPIOP_CALLBACK_URL_BULK_TRANSFER_POST", "FSPIOP_CALLBACK_URL_BULK_TRANSFER_PUT", "FSPIOP_CALLBACK_URL_BULK_TRANSFER_ERROR", "NET_DEBIT_CAP_THRESHOLD_BREACH_EMAIL", "NET_DEBIT_CAP_ADJUSTMENT_EMAIL", "SETTLEMENT_TRANSFER_POSITION_CHANGE_EMAIL"]

paired_enpoint_types = [(endpoint_type, endpoint_type) for endpoint_type in enpoint_types_field_list]

limit_types_field_list = ["NET_DEBIT_CAP"]

paired_limit_types = [(limit_type, limit_type) for limit_type in limit_types_field_list]

class CreateParticipantForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="Name")
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")

class InitialPositionAndLimitForm(forms.Form):
    initial_position = forms.IntegerField(required=True, label="Initial Position", initial=0)
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")
    limit_type = forms.ChoiceField(choices=paired_limit_types, required=True, label="Limit type")
    limit_value = forms.FloatField(required=True, label="Limit value", min_value=0)

class LimitForm(forms.Form):
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")
    limit_type = forms.ChoiceField(choices=paired_limit_types, required=True, label="Limit type")
    limit_value = forms.FloatField(required=True, label="Limit value", min_value=0)
    alarm_percentage = forms.FloatField(required=True, label="Alarm Percentage", min_value=0)

class ParticipantEndpointForm(forms.Form):
    type = forms.ChoiceField(choices=paired_enpoint_types, label="Type", required=True)
    value = forms.CharField(required=True, label="Value", max_length=255)

class ParticipantAccountForm(forms.Form):
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")
    type = forms.ChoiceField(choices=[("INTERCHANGE_FEE", "INTERCHANGE_FEE"), ("POSITION", "POSITION"), ("SETTLEMENT", "SETTLEMENT")], label="Type", required=True)

class HubAccountForm(forms.Form):
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")
    type = forms.ChoiceField(choices=[("HUB_MULTILATERAL_SETTLEMENT", "HUB_MULTILATERAL_SETTLEMENT"), ("HUB_RECONCILIATION", "HUB_RECONCILIATION")], label="Type", required=True)

class SettlementModelsForm(forms.Form):
    name = forms.CharField(max_length=255, label="Name", required=True)
    settlementGranularity = forms.ChoiceField(choices=[("GROSS", "GROSS"), ("NET", "NET")], label="Granularity", required=True)
    settlementInterchange = forms.ChoiceField(choices=[("BILATERAL", "BILATERAL"), ("MULTILATERAL", "MULTILATERAL")], label="Interchange", required=True)
    settlementDelay = forms.ChoiceField(choices=[("DEFERRED", "DEFERRED"), ("IMMEDIATE", "IMMEDIATE")], label="Delay", required=True)
    requireLiquidityCheck = forms.ChoiceField(choices=[("False", "False"), ("True", "True")], label="Require Liquidity Check", required=True)
    ledgerAccountType = forms.ChoiceField(choices=[("INTERCHANGE_FEE", "INTERCHANGE_FEE"), ("POSITION", "POSITION")], label="Ledger Account Type", required=True)
    autoPositionReset = forms.ChoiceField(choices=[("False", "False"), ("True", "True")], label="Automatic Position Reset", required=True)
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")
    settlementAccountType = forms.ChoiceField(choices=[("POSITION", "POSITION"), ("SETTLEMENT", "SETTLEMENT"), ("INTERCHANGE_FEE_SETTLEMENT", "INTERCHANGE_FEE_SETTLEMENT")], label="Settlement Account Type", required=True)

class RecordTransactionForm(forms.Form):
    transfer_id = forms.CharField(max_length=255, required=True, label="Transfer ID")
    external_reference = forms.CharField(required=True, max_length=100, label="External Reference")
    action = forms.ChoiceField(choices=[("recordFundsIn", "recordFundsIn"), ("recordFundsOutPrepareReserve", "recordFundsOutPrepareReserve")], label="Action", required=True)
    amount = forms.FloatField(label="Amount", min_value=0);
    currency = forms.ChoiceField(choices=paired_currencies, required=True, label="Currency")