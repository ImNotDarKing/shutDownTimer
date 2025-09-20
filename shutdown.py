import subprocess
import tkinter as tk
from tkinter import messagebox

def start_timer():
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return

    if hours <= 0  and minutes < 20:
        minutes = 20

    seconds = hours * 3600 + minutes * 60
    if not (0 < seconds <= 72000):
        messagebox.showerror("Ошибка", "Введите корректное время (1 сек – 20 часов)")
        return

    cmd = f"timeout /t {seconds} /nobreak && shutdown {mode_var.get()}"
    subprocess.Popen(["cmd", "/c", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    root.withdraw()
    # root.iconify()

def change_value(entry, delta):
    try:
        value = int(entry.get())
    except ValueError:
        value = 0
    value = max(0, value + delta)
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

root = tk.Tk()
root.title("Shutdown Timer")
root.geometry("260x230")

def add_field(label_text):
    tk.Label(root, text=label_text).pack()
    frame = tk.Frame(root); frame.pack()
    entry = tk.Entry(frame, width=5, justify="center"); entry.insert(0, "0")
    tk.Button(frame, text="-", width=3, command=lambda: change_value(entry, -1), bg='darksalmon').pack(side="left")
    entry.pack(side="left")
    tk.Button(frame, text="+", width=3, command=lambda: change_value(entry, 1), bg='darkolivegreen2').pack(side="left")
    return entry

hours_entry = add_field("Часы:")
minutes_entry = add_field("Минуты:")

mode_var = tk.StringVar(value="/h")
for text, val in [("Гибернация", "/h"), ("Выключение", "/s"), ("Перезагрузка", "/r")]:
    tk.Radiobutton(root, text=text, variable=mode_var, value=val).pack()

tk.Button(root, text="Запустить", command=start_timer, bg='gold1').pack(pady=10)

root.mainloop()
