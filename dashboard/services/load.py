from dashboard.models import Price, Balance, Metadata
from django.db import connection

def load_prices(df):
    connection.close()
    connection.connect()
    
    records = []
    
    for _, row in df.iterrows():
        records.append(
            Price(
                timestamp=row["timestamp"],
                symbol=row["symbol"],
                price_USD=row["price_USD"],
            )
        )

    print("Creating Price objects in the dataframe")

    Price.objects.bulk_create(records, ignore_conflicts=True)

def load_metadata(df):

    connection.close()
    connection.connect()

    records = []

    for _, row in df.iterrows():
        records.append(
            Metadata(
                address=row["address"],
                name=row["name"],
                symbol=row["symbol"],
                decimals=row["decimals"],
            )
        )
    
    print("Creating Metadata objects in the dataframe")

    Metadata.objects.bulk_create(records, batch_size=100, ignore_conflicts=True)


def load_balances(df):

    connection.close()
    connection.connect()
    
    records = []

    for _, row in df.iterrows():
        records.append(
            Balance(
                timestamp=row["timestamp"],
                wallet=row["wallet"],
                contract_address=row["contract_address"],
                symbol=row["symbol"],
                name=row["name"],
                raw_balance=row["raw_balance"],
                decimals=row["decimals"],
                adjusted_balance=row["adjusted_balance"],
            )
        )
    
    print("Creating Balance objects in the dataframe")

    Balance.objects.bulk_create(records, ignore_conflicts=True)