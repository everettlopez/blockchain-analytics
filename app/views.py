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

    wallet_address = "0x1E6E8695FAb3Eb382534915eA8d7Cc1D1994B152"

    data = fetch_tokens_by_wallet(wallet_address)

    addresses = data.get("addresses", []) 
    takens_by_wallet = data.get("tokens", [])

    token_map = {}

    for t in takens_by_wallet:
        meta = t.get("tokenMetadata", {})
        symbol = meta.get("symbol")


        if symbol:
            token_map[symbol] = t 

    return render(request, "dashboard.html", {
        "takens_by_wallet": token_map,
        "wallet_address": wallet_address
    })