import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def linear_func(x, a, b):
    return a * x + b

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.csv;*.dat;*.txt")])
    if file_path:
        file_entry.config(state=tk.NORMAL)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_entry.config(state=tk.DISABLED)

def save_graph():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("PDF", "*.pdf")])
    if save_path:
        fig.savefig(save_path)
        messagebox.showinfo("Success", "Graph saved successfully.")

def load_data():
    if not file_path:
        messagebox.showerror("Error", "Please select a data file.")
        return None, None
    try:
        delimiter = delimiter_entry.get().strip() or ","
        data = pd.read_csv(file_path, delimiter=delimiter, header=None)
        data = data.dropna().reset_index(drop=True)
        
        if data.shape[1] < 2:
            messagebox.showerror("Error", "The file must have at least two columns.")
            return None, None
        
        return data.iloc[:, 0].values, data.iloc[:, 1].values
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        return None, None

def save_fitted_data():
    x, y = load_data()
    if x is None or y is None:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if save_path:
        fitted_data = pd.DataFrame({"X": x, "Y": y})
        fitted_data.to_csv(save_path, index=False)
        messagebox.showinfo("Success", "Fitted data saved successfully.")

def plot_data():
    x, y = load_data()
    if x is None or y is None:
        return
    
    fig.clear()
    ax = fig.add_subplot(111)
    ax.scatter(x, y, label="Data")
    ax.set_xlabel(x_label_entry.get() or "X-axis")
    ax.set_ylabel(y_label_entry.get() or "Y-axis")
    ax.set_title(title_entry.get() or "Data Plot")
    ax.legend()
    canvas.draw()

def fit_data():
    x, y = load_data()
    if x is None or y is None:
        return
    try:
        x_min, x_max = float(x_min_entry.get()), float(x_max_entry.get())
        mask = (x >= x_min) & (x <= x_max)
        x_fit, y_fit = x[mask], y[mask]
        
        if len(x_fit) < 2:
            messagebox.showerror("Error", "Not enough data points in the selected range for fitting.")
            return
        
        popt, _ = curve_fit(linear_func, x_fit, y_fit)
        y_pred = linear_func(x_fit, *popt)
        
        fig.clear()
        ax = fig.add_subplot(111)
        ax.scatter(x, y, label="Original Data", alpha=0.5)
        ax.plot(x_fit, y_pred, color='red', label=f"Fit: y={popt[0]:.2f}x+{popt[1]:.2f}")
        ax.set_xlabel(x_label_entry.get() or "X-axis")
        ax.set_ylabel(y_label_entry.get() or "Y-axis")
        ax.set_title(title_entry.get() or "Linear Fit")
        ax.legend()
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Graph Plotter")
root.geometry("900x600")

menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=select_file)
file_menu.add_command(label="Save Graph", command=save_graph)
file_menu.add_command(label="Save Fitted Data", command=save_fitted_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

frame_top = tk.Frame(root)
frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

tk.Label(frame_top, text="File:").grid(row=0, column=0, padx=5)
file_entry = tk.Entry(frame_top, width=60, state=tk.DISABLED)
file_entry.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Delimiter:").grid(row=0, column=2, padx=5)
delimiter_entry = tk.Entry(frame_top, width=5)
delimiter_entry.grid(row=0, column=3, padx=5)

tk.Button(frame_top, text="Plot Data", command=plot_data).grid(row=0, column=4, padx=5)

tk.Label(frame_top, text="X Label:").grid(row=1, column=0, padx=5)
x_label_entry = tk.Entry(frame_top, width=15)
x_label_entry.grid(row=1, column=1, padx=5)

tk.Label(frame_top, text="Y Label:").grid(row=1, column=2, padx=5)
y_label_entry = tk.Entry(frame_top, width=15)
y_label_entry.grid(row=1, column=3, padx=5)

tk.Label(frame_top, text="Title:").grid(row=1, column=4, padx=5)
title_entry = tk.Entry(frame_top, width=20)
title_entry.grid(row=1, column=5, padx=5)

frame_fit = tk.Frame(root)
frame_fit.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

tk.Label(frame_fit, text="Fit Range Xmin:").grid(row=0, column=0, padx=5)
x_min_entry = tk.Entry(frame_fit, width=10)
x_min_entry.grid(row=0, column=1, padx=5)

tk.Label(frame_fit, text="Xmax:").grid(row=0, column=2, padx=5)
x_max_entry = tk.Entry(frame_fit, width=10)
x_max_entry.grid(row=0, column=3, padx=5)

tk.Button(frame_fit, text="Fit Data", command=fit_data).grid(row=0, column=4, padx=5)

fig = plt.Figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
