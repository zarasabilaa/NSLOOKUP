import tkinter as tk
from tkinter import ttk
import psutil # type: ignore
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
import threading
import time
import os
import sys

running = False

def monitor_bandwidth():
    old_sent = psutil.net_io_counters().bytes_sent
    old_recv = psutil.net_io_counters().bytes_recv

    while running:
        time.sleep(0.2)

        new_sent = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv

        upload_speed = (new_sent - old_sent) / 1024
        download_speed = (new_recv - old_recv) / 1024

        old_sent = new_sent
        old_recv = new_recv

        upload_data.append(upload_speed)
        download_data.append(download_speed)

        if len(upload_data) > 50 :
            upload_data.pop(0)
            download_data.pop(0)

        update_graph()

def start_monitor():
    global running
    if not running:
        running = True
        thread = threading.Thread(target=monitor_bandwidth, daemon=True)
        thread.start()


def stop_monitor():
    global running
    running = False


def update_graph():
    ax.clear()
    ax.plot(upload_data, label="Upload (KB/s)", color="red")
    ax.plot(download_data, label="Download (KB/s)", color="blue")
    ax.set_ylabel("KB/s")
    ax.set_xlabel("Time")
    ax.legend()
    ax.set_title("Bandwidth Monitor")
    canvas.draw()


root = tk.Tk()
root.title("Bandwidth Monitor")
root.geometry("800x500")

fig, ax = plt.subplots(figsize=(7, 4))
upload_data = []
download_data = []
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

frame = ttk.Frame(root)
frame.pack(pady=10)

btn_start = ttk.Button(frame, text="Mulai", command=start_monitor)
btn_start.grid(row=0, column=0, padx=10)

btn_stop = ttk.Button(frame, text="Berhenti", command=stop_monitor)
btn_stop.grid(row=0, column=1, padx=10)


# ---- CLEAN EXIT + FORCE KILL ----
def on_closing():
    global running
    running = False
    root.destroy()
    os._exit(0)   # proses langsung selesai, prompt kembali instan


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
