import requests
from django.conf import settings

def fetch_tokens_by_wallet(wallet_address:str):
    url = f"https://api.g.alchemy.com/data/v1/s2kvq29Go01b0789itZY0/assets/tokens/by-address"

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
        "includeErc20Tokens": True
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json().get("data", {})

    return data