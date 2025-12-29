from django.db import models

class Price(models.Model):
    timestamp = models.DateTimeField()
    symbol = models.CharField(max_length=5)
    price_USD = models.FloatField()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}: ${self.price_USD}"
    
class Metadata(models.Model):
    address = models.CharField(max_length=42, unique=True)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=5)
    decimals = models.IntegerField()

    def __str__(self):
        return f"Load {self.name} {self.symbol} metadata."

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
        return f"{self.wallet} holds {self.adjusted_balance} of {self.symbol}"
    

