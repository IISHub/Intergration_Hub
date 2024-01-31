from django.urls import path
from .views import payment_manager, central_ledger

urlpatterns = [
    path('sendmoney/', payment_manager.send_money),
    path('parties/', payment_manager.get_party),
    path('quotes/', payment_manager.get_quote),
    path('transfer/', payment_manager.accept_or_decline_transfer),

    path('', central_ledger.get_participants, name="dashboard"),
    path('participant/create', central_ledger.create_participant, name="create-participant"),
    path('participant/<str:name>', central_ledger.view_participant, name="get-participant"),
]