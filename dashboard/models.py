from django.db import models

class Price(models.Model):
    timestamp = models.DateTimeField()
    symbol = models.CharField(max_length=10)
    price_USD = models.FloatField()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}: {self.price_usd}"
