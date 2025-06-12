import tkinter as tk
import tkinter as ttk, messagebox
import json
import time
import threading
import random

DATA_FILE = "equities.json"

def fetch_mock_api(symbol):
  return{
    "price" : 100
  }


def mock_chatgpt_response(message):
  return f"Mock response to : {message}"

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
    self.symbol_entry.grid(row=1, column=3)

    tk.Label(self.form_frame, text="Symbol:").grid(row=0, column=4)
    self.drawdown_entry = tk.Entry(self.form_frame)
    self.drawdown_entry_grid(row=1,column=5)

    #table to track the traded equities
    self.tree = ttk.Treeview(root,columns = ("Symbol", "Position", "Entry Price", "Levels", "Status"),show = 'headings')
    for col in ["Symbol", "Position", "Entry Price", "Levels", "Status"]
      self.tree.heading(col, text=col)
      self.tree.column(col, witdth =120)
    self.tree.pack(pady=10)
