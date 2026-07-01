import subprocess
# import os
import tkinter as tk
from tkinter import messagebox

def start_timer():
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return

    mode = mode_var.get()

    # if mode == "shutdown" or mode == "restart":
    #     if hours == 0 and minutes < 20 and minutes != 0:
    #         minutes = 20

    if hours == 0 and minutes == 0:
        messagebox.showerror("Ошибка", "Введите хотя бы 1 минуту")
        return


    seconds = hours * 3600 + minutes * 60
    if not (0 < seconds <= 72000):
        messagebox.showerror("Ошибка", "Введите корректное время (1 минута – 20 часов)")
        return
    
    if mode == "hibernate":
        cmd = f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState Hibernate"
    elif mode == "sleep":
        cmd = f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState Sleep"
    # elif mode == "shutdown":
    #     cmd = f"timeout /t {seconds} /nobreak && shutdown /s"
    # elif mode == "restart":
    #     cmd = f"timeout /t {seconds} /nobreak && shutdown /r"
    else:
        messagebox.showerror("Ошибка", "Не выбран режим")
        return

    if mode == "hibernate" or mode == "sleep": 
        subprocess.Popen(["cmd", "/c", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    # elif mode == "shutdown" or mode == "restart":
        # os.system(f'start cmd /c "{cmd}"')
        
    root.withdraw()


def change_focused(delta):
    # delta: 1 = вправо (плюс), -1 = влево (минус)
    if root.focus_get() == hours_entry:
        change_value(hours_entry, delta)
    
    elif root.focus_get() == minutes_entry:
        change_value(minutes_entry, delta)
    

def switch_focus(direction):
    if direction == -1:  # вверх - на часы
        hours_entry.focus_set()
    elif direction == 1:  # вниз - на минуты
        minutes_entry.focus_set()


def change_value(entry, delta):
    try:
        value = int(entry.get())
    except ValueError:
        value = 0
    
    # Ограничения для часов
    if entry == hours_entry:
        value = max(0, min(20, value + delta)) 
    # Ограничения для минут
    elif entry == minutes_entry:
        if int(hours_entry.get() or 0) == 20:
            value = 0          
        else:
            value = max(0, min(59, value + delta))
    
    entry.delete(0, tk.END)
    entry.insert(0, str(value))


root = tk.Tk()
root.title("Shutdown Timer")
root.geometry("200x220")
root.resizable(False, False)

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
hours_entry.focus_set()

# Отступ между Sleep и Minutes
tk.Frame(root, height=15).pack() 

mode_var = tk.StringVar(value="sleep")
modes = [
    ("Сон", "sleep"),
    ("Гибернация", "hibernate"),
    # ("Выключение", "shutdown"),
    # ("Перезагрузка", "restart"),
]

for text, val in modes:
    tk.Radiobutton(root, text=text, variable=mode_var, value=val).pack()

tk.Button(root, text="Запустить", command=start_timer, bg='gold1').pack(pady=10)

root.bind('<Left>', lambda e: change_focused(-1))
root.bind('<Right>', lambda e: change_focused(1))
root.bind('<Up>', lambda e: switch_focus(-1))
root.bind('<Down>', lambda e: switch_focus(1))
root.bind('<Return>', lambda e: start_timer())

root.mainloop()