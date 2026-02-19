import requests
from django.conf import settings

def fetch_tokens_by_wallet(wallet_address:str):
    url = f"https://api.g.alchemy.com/data/v1/{settings.ALCHEMY_API_KEY}/assets/tokens/by-address"

    payload = {
        "addresses": [
            {
                "address": wallet_address,
                "networks": ["eth-mainnet"]
            }
        ],
        "withMetadata": True,
        "withPrices": True,
        "includeNativeTokens": True,
        "includeErc20Tokens": True,
        "pageKey": "string"
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json().get("data", {})

    return data