import pandas as pd

def load_raw_prices(path="data/prices.jsonl"):
    return pd.read_json(path, lines=True)

def normalize_prices(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.rename(columns={'data': 'price_USD'})
    df = df.sort_values(by='timestamp')
    
    return df[["timestamp", "symbol", "price_USD"]]

def load_metadata(path="data/metadata.jsonl"):
    return pd.read_json(path, lines=True)

def normalize_metadata(df):
    decimal_list = df["data"].apply(lambda x: x["result"]["decimals"])
    token_symbol_list = df["data"].apply(lambda x: x["result"]["symbol"])
    token_name_list = df["data"].apply(lambda x: x["result"]["name"])

    decimal = decimal_list.explode().reset_index(drop=True)
    decimal = decimal.apply(pd.Series)
    decimal["symbol"] = token_symbol_list
    decimal["name"] = token_name_list
    decimal["address"] = df["address"]
    decimal["decimals"] = decimal[0]

    return decimal[["address", "name", "symbol", "decimals"]]