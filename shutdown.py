import subprocess
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def start_action():
    if mode_type_var.get() == "timer":
        start_timer()
    else:
        start_alarm()


def start_timer():
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return

    if hours == 0 and minutes == 0:
        messagebox.showerror("Ошибка", "Введите хотя бы 1 минуту")
        return

    seconds = hours * 3600 + minutes * 60

    if not (0 < seconds <= 72000):
        messagebox.showerror("Ошибка", "Введите корректное время (1 минута – 20 часов)")
        return

    execute_action(seconds)


def start_alarm():
    try:
        hours = int(alarm_hours_entry.get())
        minutes = int(alarm_minutes_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return

    if not (0 <= hours <= 23):
        messagebox.showerror("Ошибка", "Часы должны быть 0-23")
        return

    if not (0 <= minutes <= 59):
        messagebox.showerror("Ошибка", "Минуты должны быть 0-59")
        return

    now = datetime.now()
    target = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)

    if target <= now:
        target += timedelta(days=1)

    seconds = int((target - now).total_seconds())

    if seconds > 72000:
        messagebox.showerror("Ошибка", "Максимум 20 часов")
        return

    execute_action(seconds)


def execute_action(seconds):
    mode = mode_var.get()

    if mode == "hibernate":
        cmd = f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState Hibernate"
    else:
        cmd = f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState Sleep"

    subprocess.Popen(["cmd", "/c", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    root.withdraw()


def change_value(entry, delta, max_val, min_val=0):
    try:
        value = int(entry.get())
    except ValueError:
        value = 0

    if entry == minutes_entry:
        try:
            h = int(hours_entry.get())
        except:
            h = 0

        if h >= 20:
            max_val = 0

    value += delta

    if value < min_val:
        value = min_val
    if value > max_val:
        value = max_val

    entry.delete(0, tk.END)
    entry.insert(0, str(value))


def change_focused(delta):
    focused = root.focus_get()

    if mode_type_var.get() == "timer":
        if focused == hours_entry:
            change_value(hours_entry, delta, 20)
        elif focused == minutes_entry:
            change_value(minutes_entry, delta, 59)
    else:
        if focused == alarm_hours_entry:
            change_value(alarm_hours_entry, delta, 23)
        elif focused == alarm_minutes_entry:
            change_value(alarm_minutes_entry, delta, 59)


def switch_focus(direction):
    if mode_type_var.get() == "timer":
        if direction == -1:
            hours_entry.focus_set()
        else:
            minutes_entry.focus_set()
    else:
        if direction == -1:
            alarm_hours_entry.focus_set()
        else:
            alarm_minutes_entry.focus_set()


def toggle_mode():
    if mode_type_var.get() == "timer":
        timer_frame.place(relx=0.5, rely=0.5, anchor="center")
        alarm_frame.place_forget()
        hours_entry.focus_set()
    else:
        alarm_frame.place(relx=0.5, rely=0.5, anchor="center")
        timer_frame.place_forget()
        alarm_hours_entry.focus_set()


def add_field(parent, label, max_value):
    tk.Label(parent, text=label).pack()

    frame = tk.Frame(parent)
    frame.pack()

    tk.Button(
        frame,
        text="-",
        width=3,
        bg="darksalmon",
        command=lambda: change_value(entry, -1, max_value)
    ).pack(side="left")

    entry = tk.Entry(frame, width=5, justify="center")
    entry.insert(0, "0")
    entry.pack(side="left")

    tk.Button(
        frame,
        text="+",
        width=3,
        bg="darkolivegreen2",
        command=lambda: change_value(entry, 1, max_value)
    ).pack(side="left")

    return entry


root = tk.Tk()
root.title("Shutdown Timer")
root.geometry("230x300")
root.resizable(False, False)

tk.Label(root, text="Режим:", font=("Arial", 9, "bold")).pack()

mode_type_var = tk.StringVar(value="timer")

tk.Radiobutton(
    root,
    text="Таймер (через)",
    variable=mode_type_var,
    value="timer",
    command=toggle_mode
).pack()

tk.Radiobutton(
    root,
    text="Будильник (в)",
    variable=mode_type_var,
    value="alarm",
    command=toggle_mode
).pack()



content = tk.Frame(root, width=210, height=120)
content.pack()

content.pack_propagate(False)

timer_frame = tk.Frame(content)
alarm_frame = tk.Frame(content)

hours_entry = add_field(timer_frame, "Часы:", 20)
minutes_entry = add_field(timer_frame, "Минуты:", 59)

alarm_hours_entry = add_field(alarm_frame, "Часы (0-23):", 23)
alarm_minutes_entry = add_field(alarm_frame, "Минуты (0-59):", 59)

timer_frame.place(relx=0.5, rely=0.5, anchor="center")

mode_var = tk.StringVar(value="sleep")

tk.Radiobutton(root, text="Сон", variable=mode_var, value="sleep").pack()
tk.Radiobutton(root, text="Гибернация", variable=mode_var, value="hibernate").pack()

tk.Button(
    root,
    text="Запустить",
    command=start_action,
    bg="gold1"
).pack(pady=10)

root.bind("<Left>", lambda e: change_focused(-1))
root.bind("<Right>", lambda e: change_focused(1))
root.bind("<Up>", lambda e: switch_focus(-1))
root.bind("<Down>", lambda e: switch_focus(1))
root.bind("<Return>", lambda e: start_action())

hours_entry.focus_set()

root.mainloop()