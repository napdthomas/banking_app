# finance/monzo_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.transactions_list, name='transactions_list'),
]