from django.urls import path
from .views import payment_manager, central_ledger

urlpatterns = [
    path('sendmoney/', payment_manager.send_money),
    path('parties/', payment_manager.get_party),
    path('quotes/', payment_manager.get_quote),
    path('transfer/', payment_manager.accept_or_decline_transfer),

    path('', central_ledger.get_participants, name="dashboard"),
    path('participant/limits', central_ledger.create_participant, name="participants-limits"),
    path('participant-limit', central_ledger.get_participants_limits, name="participant-limit"),
    path('participant/create', central_ledger.create_participant, name="create-participant"),
    path('participant/<str:name>', central_ledger.view_participant, name="get-participant"),
    path('participant/<str:name>/activity/<str:activity>', central_ledger.update_participant_activity, name="update-participant-activity"),
]