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

    self.add_button = tk.Button(self.form_frame, text ="Add Equity", command=self.add_equity)
    self.add_button(row=0, column=6)
    
    #table to track the traded equities
    self.tree = ttk.Treeview(root,columns = ("Symbol", "Position", "Entry Price", "Levels", "Status"),show = 'headings')
    for col in ["Symbol", "Position", "Entry Price", "Levels", "Status"]
      self.tree.heading(col, text=col)
      self.tree.column(col, witdth =120)
    self.tree.pack(pady=10)

    #control 
    self.toggle_system_button = tk.Button(root,text="Toggle Selected System", command=self.toggle_system)
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
