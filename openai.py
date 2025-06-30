import openai
import alpaca_trade_api as tradeapi

key = ""
secret_key=""
BASE_URL="https://paper-api.alpaca.markets/"

api=tradeapi.REST(key,secret_key,BASE_URL,api_version="v2")

def fetch_portfolio():
  positions = api.list_positions()
  portfolio = []
  for pos in positions:
    portfolio.append({
      'symbol' : pos.symbol,
      'qty' : pos.qty,
      'entry_price':pos.avg_entry_price,
      'current_price':pos.current_price,
      'unrealized_p1':pos.unrealized_p1,
      'side':'long'
    })
  return portfolio

def fetch_open_orders():
  orders = api.list_orders(status='open')
  open_orders = []
  for order in orders:
    open_orders.append({
      'symbol':order.symbol,
      'qty':order.qty,
      'limit_price':order.limit_price,
      'side':'buy'
    })
  

def analyze_message(message):
  portfolio_data = fetch_portfolio()
  open_orders = fetch_open_orders()
  pre_prompt = f"""
  You are an AI Portfolio manager responsible for analyzing my portfoilo.
  Your Tasks are the following:
  1.)Evaluate risk exposures of my current holdings
  2.)Analyze my open limit ordes and their potential impact
  3.)Provide insights into portfolio health, diversification, trade adj. etc.
  4.) Speculate on the market outlook based on current market conditions
  5.) Indentifying potential market risks and suggest risk management strategies

  Here is my portfolio: {portfolio_data)
  Here are my open orders {open_ordrs}

  Overall, answer the follwojng question with priority having that background:{message}
  """
  respons= openai.ChatCompletion.create(
    model="gpt-4.1"
    messages={{"role":"system", "content":pre_prompt}],
    api_key= ""
  )
  return response['choices'][0]['message']['content']

analysis = analyze_message("How is my portfolio doing?")
