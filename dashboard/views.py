from django.shortcuts import render

from django.http import JsonResponse 
from .models import Balance, Metadata, Price
import json


def index(request):
    tokens = ["BTC", "ETH", "LINK", "BNB", "USDT", "USDC"]

    latest_prices = {}
    

    for symbol in tokens:
        price = Price.objects.filter(symbol=symbol).order_by("-timestamp").first()
        latest_prices[symbol] = price.price_USD if price else None
    return render(request, "index.html", {
        "latest_prices":latest_prices
    })

def login(request):
    return render(request, "login.html")

def dashboard(request): 
    prices = Price.objects.filter(symbol="ETH").order_by("-timestamp") 
    eth_prices_json = json.dumps([ { "timestamp": p.timestamp.isoformat(), "price": float(p.price_USD) } for p in prices ]) 
    return render(request, "dashboard.html", {"eth_prices_json": eth_prices_json})


def get_latest_balances(request):
    data = list(
        Balance.objects.order_by("-timestamp")[:20].values()
    )
    return JsonResponse(data, safe=False)

def get_token_metadata(request):
    data = list(
        Metadata.objects.values()
    )
    return JsonResponse(data, safe=False)

def get_token_prices(request):
    data = list(
        Price.objects.order_by("-timestamp")[:20].values()
    )
    return JsonResponse(data, safe=False)