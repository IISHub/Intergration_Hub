from django.urls import path
from . import views

urlpatterns = [
    path('sendmoney/', views.send_money),
    path('parties/', views.get_party),
    path('quotes/', views.get_quote),
    path('transfer/', views.accept_or_decline_transfer),
]