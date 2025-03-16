import os
from dotenv import load_dotenv 
load_dotenv()
import time
import subprocess
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

if 'METABASE_PATH' in os.environ:
    METABASE_PATH = os.environ['METABASE_PATH']
else:
    METABASE_PATH = r"C:\Users\Judah\My Drive\Programming\StatBucketWebApp\backend\metabase\metabase.jar"


class FrontendState():
    frontend_started = False
    
    _metabase_popen: subprocess.Popen | None = None
    _ngrok_popen: subprocess.Popen | None = None
    
    @classmethod
    def _start_frontend(cls):
        # Run this in the background
        cls._metabase_popen = subprocess.Popen(f'java -jar "{METABASE_PATH}"', shell=True)
        cls._ngrok_popen = subprocess.Popen('ngrok http --domain=judahwilson.ngrok.io 3000')
        
    @classmethod
    def _stop_frontend(cls):
        cls._metabase_popen.terminate()
        cls._ngrok_popen.terminate()
        
    @classmethod
    def toggle_frontend(cls):
        if not cls.frontend_started:
            FrontendState._start_frontend()
            cls.frontend_started = True
            btn['text'] = "Stop Frontend"
        else:
            FrontendState._stop_frontend()
            cls.frontend_started = False
            btn['text'] = "Start Frontend"
    
    
# TODO implement tkinter GUI
root = ThemedTk(theme="arc")
root.title("StatBucket Admin")

# Create a tabbed notebook interface
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# region Tab basic
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Basic')
ttk.Label(tab1, text='Text Input:').grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
ttk.Entry(tab1).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(tab1, text='Password:').grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
ttk.Entry(tab1, show='*').grid(row=1, column=1, padx=10, pady=5)

ttk.Label(tab1, text='Check:').grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
ttk.Checkbutton(tab1).grid(row=0, column=3, padx=10, pady=5)

ttk.Label(tab1, text='Radio:').grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)
r_var = tk.IntVar()
ttk.Radiobutton(tab1, text="Option 1", variable=r_var, value=1).grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)
ttk.Radiobutton(tab1, text="Option 2", variable=r_var, value=2).grid(row=2, column=3, sticky=tk.W, padx=10, pady=5)

btn = ttk.Button(tab1, text="Start Frontend", command=FrontendState.toggle_frontend)
btn.grid(row=4, column=0, columnspan=2, pady=20)
#endregion


root.mainloop()