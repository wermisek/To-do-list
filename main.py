import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import scrolledtext
import re
from datetime import datetime

zadania = {}

def zapisz_zadanie():
    data = kalendarz.get_date()
    zadanie = entry.get()
    godzina = entry_godzina.get()
    
    if data in zadania and zadanie in zadania[data]:
        messagebox.showwarning("Error", "You can add one date to one task")
    elif zadanie:
        if is_valid_time(godzina):  
            if godzina:
                godzina = standardize_time_format(godzina) 
                zadanie = f"{zadanie} - {godzina}"
            
            if data in zadania:
                zadania[data].append(zadanie)
            else:
                zadania[data] = [zadanie]
            
            entry.delete(0, tk.END)
            entry_godzina.delete(0, tk.END)  
            scrolled_text.delete(1.0, tk.END)  
            for data, lista in zadania.items():
                for zadanie in lista:
                    scrolled_text.insert(tk.END, f"{data}: {zadanie}\n")
        else:
            messagebox.showwarning("Error", "Type correct hour (format HH:MM lub H.MM)")

def is_valid_time(time_str):
    pattern = r"^(0?[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|^[0-9]+(\.[0-5][0-9])?$"
    return re.match(pattern, time_str)

def standardize_time_format(time_str):
    if '.' in time_str:
        parts = time_str.split('.')
        hours = parts[0]
        minutes = parts[1]
        return f"{hours.zfill(2)}.{minutes.zfill(2)}"
    else:
        parts = time_str.split(':')
        hours = parts[0]
        minutes = parts[1]
        return f"{hours.zfill(2)}:{minutes.zfill(2)}"

def usun_zadanie():
    try:
        wybrane = scrolled_text.tag_ranges(scrolled_text.tag_names())
        data, _ = scrolled_text.get(wybrane[0], wybrane[-1]).split(":")
        del zadania[data]
        scrolled_text.delete(wybrane[0], wybrane[-1])
    except:
        messagebox.showwarning("Error", "Choose which task you want to delete!")

def na_wejscie_godzina(event):
    if entry_godzina.get() == "Hour":
        entry_godzina.delete(0, tk.END)

def na_wyjscie_godzina(event):
    if not entry_godzina.get():
        entry_godzina.insert(0, "Hour")

def zapisz_zadania_przed_zamknieciem():
    zapisz_do_pliku()
    root.destroy()

def zapisz_do_pliku():
    today = datetime.today()
    data = today.strftime("%Y-%m-%d")
    file_name = f"To-do List {data}.txt"
    with open(file_name, "w") as file:
        for data, lista in zadania.items():
            for zadanie in lista:
                file.write(f"{data}: {zadanie}\n")

root = tk.Tk()
root.title("To-do List")
root.geometry("600x600")
root.protocol("WM_DELETE_WINDOW", zapisz_zadania_przed_zamknieciem)

frame = tk.Frame(root)
frame.pack(pady=10)

kalendarz = Calendar(frame, selectmode="day", date_pattern="yyyy-mm-dd")
kalendarz.pack()

entry = tk.Entry(frame, font=("Helvetica", 16), width=35)
entry.pack()

entry_godzina = tk.Entry(frame, font=("Helvetica", 16), fg="grey", width=35)
entry_godzina.insert(0, "Hour")
entry_godzina.pack()

entry_godzina.bind("<FocusIn>", na_wejscie_godzina)
entry_godzina.bind("<FocusOut>", na_wyjscie_godzina)

przycisk_dodaj = tk.Button(frame, text="Add task", font=("Helvetica", 16), command=zapisz_zadanie)
przycisk_dodaj.pack()

przycisk_usun = tk.Button(root, text="Delete task", font=("Helvetica", 16), command=usun_zadanie)
przycisk_usun.pack(pady=10)

scrolled_text = scrolledtext.ScrolledText(root, font=("Helvetica", 16), selectbackground="yellow", wrap=tk.WORD)
scrolled_text.pack(expand=True, fill='both')

root.mainloop()
