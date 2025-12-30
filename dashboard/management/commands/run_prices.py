from django.core.management.base import BaseCommand
from dashboard.services.transform import load_raw_prices, normalize_prices
from dashboard.services.load import load_prices
from dashboard.services.ingestion import fetch_token_prices

class Command(BaseCommand):
    help = "Fetch, normalize, and load token prices"

    def handle(self, *args, **kwargs):

        token_symbols = [
        "BNB",
        "LINK",
        "USDT",
        "USDC",
        "ETH",
        "BTC"
        ]

        for symbol in token_symbols:
            fetch_token_prices(symbol)


        raw = load_raw_prices()
        normalized = normalize_prices(raw)
        
        load_prices(normalized)
        self.stdout.write(self.style.SUCCESS("Price ETL completed"))
