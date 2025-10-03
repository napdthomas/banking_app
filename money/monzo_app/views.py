# finance/monzo_app/views.py
import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

def transactions_list(request):
    access_token = os.getenv('MONZO_ACCESS_TOKEN')
    api_url = os.getenv('MONZO_API_URL', 'https://api.monzo.com')
    if not access_token:
        return HttpResponse('MONZO_ACCESS_TOKEN not set', status=500)

    headers = {'Authorization': f'Bearer {access_token}'}

    # Get accounts
    accounts_resp = requests.get(f'{api_url}/accounts', headers=headers)
    if accounts_resp.status_code != 200:
        return HttpResponse('Failed to fetch accounts', status=accounts_resp.status_code)
    accounts = accounts_resp.json().get('accounts', [])
    if not accounts:
        return HttpResponse('No accounts found', status=404)
    account_id = accounts[0]['id']

    # Get transactions with merchant expanded
    params = {
        'expand[]': 'merchant',
        'account_id': account_id,
    }
    tx_resp = requests.get(f'{api_url}/transactions', headers=headers, params=params)
    if tx_resp.status_code != 200:
        return HttpResponse('Failed to fetch transactions', status=tx_resp.status_code)
    transactions = tx_resp.json().get('transactions', [])

    rows = []
    for t in transactions:
        merchant = t.get('merchant') or {}
        rows.append({
            'id': t.get('id'),
            'created': t.get('created'),
            'amount': t.get('amount'),
            'currency': t.get('currency'),
            'description': t.get('description') or '',
            'merchant_name': merchant.get('name', ''),
            'merchant_category': merchant.get('category', ''),
            'is_declined': t.get('is_declined', False),
        })

    return render(request, 'monzo_app/list.html', {'rows': rows, 'account_id': account_id})
