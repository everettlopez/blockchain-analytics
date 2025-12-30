from django.db import models

class Price(models.Model):
    timestamp = models.DateTimeField()
    symbol = models.CharField(max_length=5)
    price_USD = models.FloatField()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Timestamp: {self.timestamp}\nSymbol: {self.symbol}\nPrice USD: ${self.price_USD}"
    
class Metadata(models.Model):
    address = models.CharField(max_length=42, unique=True)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=5)
    decimals = models.IntegerField()

    def __str__(self):
        return f"Token Address: {self.address}\nName: {self.name}\nSymbol: {self.symbol}\nDecimals: {self.decimals}"

class Balance(models.Model):
    timestamp = models.DateTimeField()
    wallet = models.CharField(max_length=42, unique=True)
    contract_address = models.CharField(max_length=42, unique=True)
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=30)
    raw_balance = models.IntegerField()
    decimals = models.IntegerField()
    adjusted_balance = models.FloatField()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Timestamp: {self.timestamp}\nWallet: {self.wallet}\nContract Address: {self.contract_address}\nSymbol: {self.symbol}\nName: {self.name}\nRaw Balance: {self.raw_balance}\nDecimals: {self.decimals}\nAdjusted Balance: {self.adjusted_balance}"
    

