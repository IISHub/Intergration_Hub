from django.urls import path
from .views import payment_manager, central_ledger

urlpatterns = [
    path('sendmoney/', payment_manager.send_money),
    path('parties/', payment_manager.get_party),
    path('quotes/', payment_manager.get_quote),
    path('transfer/', payment_manager.accept_or_decline_transfer),

    path('', central_ledger.dashboard, name="dashboard"),
    path('participants', central_ledger.get_participants, name="participants"),
    path('participants/limits', central_ledger.get_participants_limits, name="participants-limits"),
    path('participant/create', central_ledger.create_participant, name="create-participant"),
    path('participant/<str:name>', central_ledger.view_participant, name="get-participant"),
    path('participant/<str:name>/activity/<str:activity>', central_ledger.update_participant_activity, name="update-participant-activity"),

    path('participant/<str:name>/limits', central_ledger.update_participant_limit, name="update-participant-limit"),

    path('participant/<str:name>/endpoints', central_ledger.get_participants_endpoint, name="get-participant-endpoints"),

    path('settlementmodels', central_ledger.get_settlement_models, name="settlement-models"),
    path('settlementmodel/create', central_ledger.create_settlement_model, name="create-settlement-model"),
    path('settlementmodel/<str:name>', central_ledger.view_settlement_model, name="get-settlement-model"),
    path('settlementmodel/<str:name>/activity/<str:activity>', central_ledger.update_settlement_model_activity, name="update-settlement-model-activity"),
]