import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

from datetime import datetime
import json
import requests 
from django.conf import settings
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

token_addresses = [
        "0xB8c77482e45F1F44dE1745F52C74426C631bDD52", # BNB
        "0x514910771AF9Ca656af840dff83E8264EcF986CA", # LINK
        "0xdAC17F958D2ee523a2206206994597C13D831ec7", # USDT
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", # USDC
    ]

token_symbols = [
        "BNB",
        "LINK",
        "USDT",
        "USDC",
        "ETH",
        "BTC"
    ]

def fetch_token_balances(wallet_address):

    alchemy_url = settings.ALCHEMY_URL

    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [wallet_address, token_addresses],
        "id": 1
    }

    response = requests.post(alchemy_url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Error fetching token balances: {response.text}")
    
    data = response.json()
    save_records(wallet_address, "balances", data)

    return data


def fetch_transaction_history(wallet_address):

    alchemy_url = settings.ALCHEMY_URL

    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [{
            "fromBlock": "0x0",
            "fromAddress": "0x0000000000000000000000000000000000000000",
            "toAddress": wallet_address,
            "excludeZeroValue": True,
            "withMetadata": True,
            "category": ["erc721", "erc1155"]
        }],
        "id": 1
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(alchemy_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching transaction history: {response.text}")
    
    data = response.json()
    save_records(wallet_address, "transactions", data)

    return data

def fetch_token_metadata(contract_address):

    alchemy_url = settings.ALCHEMY_URL

    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenMetadata",
        "params": [contract_address],
        "id": 1
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(alchemy_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching token metadata: {response.text}")
    
    data = response.json()
    save_records(contract_address, "metadata", data)

    return data

def fetch_token_prices(symbol):

    cmc_url = settings.CMC_URL

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": settings.CMC_PRO_API_KEY
    }

    params = {
        "symbol": symbol,
        "convert": "USD"
    }

    response = requests.get(cmc_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Error fetching token prices: {response.text}")

    data = response.json()

    try:
        price = data["data"][symbol.upper()][0]["quote"]["USD"]["price"]
        print(f"{symbol} price: ${price:.2f}")

        save_token_prices(symbol, "prices", price)
        return price
    except KeyError:
        raise Exception(f"Price data not found for symbol: {symbol}")

def save_records(address, category, data):

    os.makedirs('data', exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "address": address,
        "data": data
    }

    with open(f"data/{category}.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")

def save_token_prices(symbol, category, data):

    os.makedirs('data', exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "data": data
    }

    with open(f"data/{category}.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")

if __name__ == "__main__":

    print("\nFetching token balances...")
    fetch_token_balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")  # Vitalik Buterin's address

    print("\nFetching transaction history...")
    fetch_transaction_history("0x5c43B1eD97e52d009611D89b74fA829FE4ac56b1") 

    print("\nFetching ETH prices...")
    for symbol in token_symbols:
        fetch_token_prices(symbol)

    print("\nFetching token metadata...")
    for token in token_addresses:
        fetch_token_metadata(token)