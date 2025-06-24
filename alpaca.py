import alpaca_trade_api as tradeapi

key = "PKBOVFA2LQAB1QPTY5HZ"
secret_key="U9FDVHrHWtKmPOuAunhXpFqb0mCfLjhzTtE7O7k0"
BASE_URL="https://paper-api.alpaca.markets/v2"

api = tradeapi.REST(key, secret_key, BASE_URL, api_version = "v2")

def get_data(symbol):
  try:
    barset = api.get_latest_trade(symbol)
    return {"price":braset.price}
  except Exception as e:
    return{"price":-1}
