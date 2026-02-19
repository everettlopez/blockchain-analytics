from django.shortcuts import render
from app.ingestion.cmc import fetch_prices
from app.ingestion.alchemy import fetch_tokens_by_wallet




def index(request):
    tokens = ["BTC", "ETH", "LINK", "DOT"]
    token_prices = fetch_prices(tokens)

    return render(request, "index.html", {
        "token_prices": token_prices
    })

def signup(request):
    return render(request, "login.html")

def dashboard(request):

    wallet_address = "0x220866B1A2219f40e72f5c628B65D54268cA3A9D"

    data = fetch_tokens_by_wallet(wallet_address)

    addresses = data.get("addresses", []) 
    tokens = addresses[0].get("tokens", []) if addresses else []

    token_map = {}

    for t in tokens:
        symbol = t["metadata"].get("symbol")

        if symbol:
            token_map[symbol] = t

    return render(request, "dashboard.html", {
        "tokens": token_map,
        "wallet_address": wallet_address
    })