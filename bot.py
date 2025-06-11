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
    
    self.symbol_label = tk.Label(self.form_frame, text="Symbol:")
    self.symbol_label.grid(row=0, column=0)
