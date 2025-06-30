import tkinter as tk
import tkinter as ttk, messagebox
import json
import time
import threading
import random
import alpaca_trade_api as tradeapi
import openai

DATA_FILE = "equities.json"

key = ""
secret_key=""
BASE_URL="https://paper-api.alpaca.markets/"

api = tradeapi.REST(key, secret_key, BASE_URL, api_version = "v2")

def fetch_portfolio():
  positions = api.list_positions()
  portfolio =[]
  for pos in positions:
    portfolio.append({
      'symbol':pos.symbol,
      'qty':pos.qty,
      'entry_price':pos.avg_entry_price,
      'current_price':pos.current_price,
      'unrealized_pl':pos.unrealized_p1,
      'side': 'buy'
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

def fetch_mock_api(symbol):
  return{
    "price" : 100
  }

def chatgpt_response(message):
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

class TradingBotGUI:
  def __init__(self, root):
    self.root = root
    self.root.title("AI Trading Bot")
    self.equities = self.load_equities()
    self.system_running = False
    
    self.form_frame = tk.Frame(root)
    self.form_frame.pack(pady=10)

    #Form to add a new equity to out trading bot
    tk.Label(self.form_frame, text="Symbol:").grid(row=0, column=0)
    self.symbol_entry = tk.Entry(self.form_frame)
    self.symbol_entry.grid(row=0, column=1)

    tk.Label(self.form_frame, text="Symbol:").grid(row=0, column=2)
    self.symbol_entry = tk.Entry(self.form_frame)
    self.symbol_entry.grid(row=0, column=3)

    tk.Label(self.form_frame, text="Symbol:").grid(row=0, column=4)
    self.drawdown_entry = tk.Entry(self.form_frame)
    self.drawdown_entry_grid(row=0,column=5)

    self.add_button = tk.Button(self.form_frame, text ="Add Equity", command=self.add_equity)
    self.add_button(row=0, column=6)
    
    #table to track the traded equities
    self.tree = ttk.Treeview(root,columns = ("Symbol", "Position", "Entry Price", "Levels", "Status"),show = 'headings')
    for col in ["Symbol", "Position", "Entry Price", "Levels", "Status"]
      self.tree.heading(col, text=col)
      self.tree.column(col, witdth =120)
    self.tree.pack(pady=10)

    #control 
    self.toggle_system_button = tk.Button(root,text="Toggle Selected System", command=self.toggle_selected_system)
    self.toggle_system_button.pack(pady=5)

    self.remove_button = tk.Button(root, text="Remove Selected Equity", command=self.remove_selected_equity)
    self.remove_button.pack(pady=5)

    #AI comp
    self.chat_frame = tk.Frame(root)
    self.chat_frame.pack(pady=10)

    self.chat_input = tk.Entry(self.chat_frame, width=50)
    self.chat_input.grid(row=0, column=0, padx=5)

    self.send_button= tk.Button(self.chat_frame, text-"send", command=self.send_message)
    self.send_button.grid(row=0, column=1)

    self.chat_output = tk.Text(root, height=5, width=60, state=tk.DISABLED)
    self.chat_output.pack()

    #load data
    self.refresh_table()

    #auto refresh
    self.running= True
    self.auto_update_thread = threading.Thread(target=self.auto_update, daemon=True)
    self.auto_update_thread.start()

  def add_equity(self):
    symbol = self.symbol_entry.get().upper()
    levels = self.levels_entry.get()
    drawdown = self.drawdown_entry.get()

      if not symbol or not levels.isdigit() or not drawdown.replace('-','',1).isdigit():
        messagebox.showerror("Error", "Invalid Input")
        return

      levels = int(levels)
      drawdown = float(drawdown)/100
      entry_price = fetch_mock_api(symbol)['price']

      level_prices= {i+1 : round(entry_price *(1-drawdown*(i+1)) ,2) for i in range(levels)}

      self.equities[symbol] = {
        "position":0,
        "entry_price":entry_price,
        "levels":level_prices,
        "drawdown" : drawdown,
        "status":"off"
      }
      self.save_equities()
      self.refresh_table()
    
  def toggle_selected_system(self):
    selected_items=self.tree.selection()
    if not selected_items:
      messagebox.showwarning("Warning","No Equity is selected")
      return

    for item in selected_items:
      symbol=self.tree.item(item)['values'][0]
      self.equities[symbol]['status'] = "on" if self.equities[symbol]['status'] == "off" else "off"

    self.save_equities()
    self.refresh_table()

  def remove_selected_equity(self):
    selected_items = self.tree.selection()
    if not selected_items:
      messagebox.showwarning("Warning", "No equity Selected")
      return
      
    for item in selected_items:
      symbol = self.tree.item(item)['values'][0]
      if symbol in self.equities:
        del self.equities[symbol]
        
    self.save_equities()
    self.refresh_table()

  def send_message(self):
    message = self.chat_input.get()
    if not message:
      return
    response = chatgpt_response(message)

    self.chat_output.config(state=tk.Normal)
    se;f.chat_output.insert(tk.END, f"You:{message}\n{response}\n\n")
    self.chat_output.config(state=tk.DISABLED)
    self.chat_input.delete(0,tk.END)

  def fetch_alpaca_data(self,symbol):
    try:
      barset=api.het_latest_trade(symbol)
      return{"price":barset.price)
    except Exception as e:
      return {"price":-1}
  
  def check_exsisting_orders(self,symbol,price):
    try:
      orders = api.list_orders(status = 'open' , symbols=symbol)
      for order in orders:
        if float(order.limit_price)== price:
          return True
    except Exception as e:
      messagebox.showerror("API Error", f"Error checking orders{e}")
    return False

  def get_max_entry_price(self, symbol):
    try:
      orders = api.list_orders(status="filled", limit=50)
      prices = [float(order.filled_avg_price) for order in orders if order.filled_avg_price and order.symbol == symbol]
      return max(prices) if prices else -1
    except Exception as e:
      messagebox.showerror("API Error", f"Error Fetching orders{e}")
    return 0
  def refresh_table(self):
    for row in self.tree.get_children():
      self.tree.delete(row)

    for symbol, data in self.equities.itmes():
      self.tree.insert("","end",values=(
        symbol,
        data['pposition'],
        data['entry_price'],
        str(data['levels']),
        data['status']
      ))
      
  def auto_update(self):
    while self.running:
      time.sleep(5)
      self.trade_systems()

  def save_equities(self):
    with open(DATA_FILE, 'w') as f:
      json.dump(self.equities,f)

  def load_equities(self):
    try:
      with open(DATA_FILE, 'r') as f:
        return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
      return{}

  def on_close(self):
    self.running = False
    self.save_equities()
    self.root.destroy()

  def trade_systems(self):
    for symbol, data in self.equities.items():
      if data['status'] == 'On'
        position_exists = False
        try:
            position = api.get_position(symbol)
            entry_price = self.get_max_entry_price(symbol)
            position_exists = True
        except Exception as e:
          api.submit_order(
            symbol = symbol,
            qty = 1,
            side="buy",
            type = "market",
            time_in_force="gtc"
          )
          messagebox.showinfo("Order Placed", f"Initial order placed for {symbol}")
          time.sleep(2)
          entry_price = self.get_max_entry_price(symbol)
        print(entry_price)
        level_prices = {i+1:round(entry_price*(1-data['drawdown']*(i+2)),2) for i in range(len(data['levels']))}
        existing_levels = self.equities.get(symbol, {}).get('levels', {})
        for levels, price in level_prices.items():
          if level not in exsisting_levels and -level not in exsisting_levels:
            exsisting_levels[level]=price
        self.equities[symbol]['entry_price'] = entry_price
        self.equities[symbol]['levels'] = exsisting_levels
        self.equities[symbol]['position'] =1

        for level, prices in level_prices.items():
          if level in self.equities[symbol]['levels']:
            self.place_order(symbol, price, level)
            
      self.save_equities()
      self.refresh_table()
  else:
      return

  def place_order(self,symbol,price,level):
    if -level in self.equities[symbol]['levels'] or '-1' in self.equities[symbol]['levels'].keys():
      return
    try:
      api.submit_order(
        symbol=symbol,
        qty =1,
        side='buy',
        type='limit',
        time_in_force='gtc',
        limit_price=price
      )
      self.equities[symbol]['levels'][-level] = price
      del self.equities[symbol]['levels'][level]
      print(f"Placed order for {symbol}@{price}")
    except Exception as e:
      messagebox.showerror("Order Error", f"Error placing order {e}")

if __name__ == '__main__' :
  root=tk.Tk()
  app = TradingBotGUI(root)
  root.protocol("WM_DELETE_WINDOW",app.on_close)
  root.miniloop()

  
