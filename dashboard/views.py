from django.shortcuts import render

from django.http import JsonResponse 
from .models import Balance, Metadata, Price

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

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