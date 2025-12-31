import pandas as pd

############ Import Data from JSONL ############

def load_raw_prices(path="data/prices.jsonl"):
    return pd.read_json(path, lines=True)

def import_metadata(path="data/metadata.jsonl"):
    return pd.read_json(path, lines=True)

def normalize_prices(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.rename(columns={'data': 'price_USD'})
    df = df.sort_values(by='timestamp')

    df["price_USD"] = df["price_USD"].round(decimals=2)
    
    return df[["timestamp", "symbol", "price_USD"]]

def import_balance(path="data/balances.jsonl"):
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

def normalize_balances(df):
    token_lists = df["data"].apply(lambda x: x["result"]["tokenBalances"])
    tokens = token_lists.explode().reset_index(drop=True)
    tokens = tokens.apply(pd.Series)
    tokens["tokenBalance"] = tokens["tokenBalance"].apply(safe_hex_to_int)

    tokens["timestamp"] = df["timestamp"].repeat(token_lists.apply(len)).values
    tokens["wallet"] = df["address"].repeat(token_lists.apply(len)).values

    tokens = tokens.rename(columns={
        "contractAddress": "contract_address",
        "tokenBalance": "raw_balance"
        })
    
    metadata_raw = import_metadata()
    decimals = normalize_metadata(metadata_raw)

    normalized_balances = apply_token_decimals(tokens, decimals)

    normalized_balances.drop_duplicates(keep="first", inplace=True)


    return normalized_balances[["timestamp", "wallet", "contract_address", "symbol", "name", "raw_balance", "decimals", "adjusted_balance"]]

def safe_hex_to_int(x):

    if isinstance(x, str) and x.startswith("0x"):
        return int(x, 16)
    return 0

def apply_token_decimals(tokens_df, decimals_df):
    merged_df = tokens_df.merge(
        decimals_df[["symbol", "name", "address", "decimals"]],
        left_on="contract_address",
        right_on="address",
        how="left"
    )

    merged_df["decimals"] = merged_df["decimals"].fillna(0).astype(int)
    merged_df["adjusted_balance"] = merged_df.apply(
        lambda row: row["raw_balance"] / (10 ** row["decimals"])
        if pd.notnull(row["decimals"]) else None,
        axis=1
    )
    
    return merged_df