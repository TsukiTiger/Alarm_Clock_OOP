import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import math


class Alarm:
    def __init__(self, window, position, time, **kw):
        super().__init__(**kw)

        self.window = window
        self.position = position
        self.time = time
        self.ONorOFF = "OFF"

        self.alarmNumber = tk.Label(self.window, text="Alarm #" + str(self.position + 1), font=("times", 20, "bold"))
        self.alarmTime = tk.Label(self.window, text=self.time, font=("times", 33, "bold"))
        self.nota = tk.Label(window, text="Hours   Minutes", font=("times", 10, "bold"))
        self.changeButton = tk.Button(self.window, text="+", font=("times", 20, "bold"),
                                      command=self.changeWindow)
        self.switchButton = tk.Button(self.window, text="OFF", font=("times", 20, "bold"), state='disable',
                                      fg="white", background="Red", command=self.switch)

        self.alarmNumber.place(x=50, y=(15 + (100 * self.position)))
        self.alarmTime.place(x=30, y=(45 + (100 * self.position)))
        self.nota.place(x=30, y=(90 + (100 * self.position)))
        self.changeButton.place(x=220, y=(50 + (100 * position)))
        self.switchButton.place(x=190, y=(20 + 100 * self.position))

        self.check_time()

    def delete(self):
        self.alarmNumber.place_forget()
        self.alarmTime.place_forget()
        self.nota.place_forget()
        self.changeButton.place_forget()
        self.switchButton.place_forget()

    def move_up(self):
        self.position -= 1
        self.alarmNumber['text'] = "Alarm #" + str(self.position + 1)
        self.alarmNumber.place(x=50, y=(15 + (100 * self.position)))
        self.alarmTime.place(x=30, y=(45 + (100 * self.position)))
        self.nota.place(x=30, y=(90 + (100 * self.position)))
        self.changeButton.place(x=220, y=(50 + (100 * self.position)))
        self.switchButton.place(x=190, y=(20 + 100 * self.position))

    def changeWindow(self):
        self.changeButton['state'] = 'disable'
        self.switchButton['state'] = 'disable'

        self.delete_button_cover = tk.Button(self.window, text="X", font=("times", 20, "bold"), fg='red',
                                             state='disable')
        position = "+250+" + str(50 + 100 * self.position)
        self.delete_button_cover.place(x=5, y=(50 + (100 * self.position)))

        self.new_window = tk.Toplevel(self.window)
        self.new_window.protocol("WM_DELETE_WINDOW", self.close_new_window_warning)
        self.new_window.geometry("400x100" + position)
        self.new_window.resizable(False, False)
        new_window_name = "Choose a New Time for Alarm # " + str(self.position + 1)
        self.new_window.title(new_window_name)

        hour_choice = []
        min_choice = []

        for hour in range(0, 24):
            if hour < 10:
                hour = f"{hour:02d}"
                hour_choice.append(hour)
            else:
                hour_choice.append(hour)

        for minute in range(0, 60, 5):
            if minute < 10:
                minute = f"{minute:02d}"
                min_choice.append(minute)
            else:
                min_choice.append(minute)

        self.hour_shown = tk.StringVar(self.new_window)
        self.hour_shown.set(self.time[:2])
        self.min_shown = tk.StringVar(self.new_window)
        self.min_shown.set(self.time[-2:])

        hour_min_label = tk.Label(self.new_window, text="Hours         Minutes", font=("times", 10, "bold"))
        hour_menu = ttk.Combobox(self.new_window, textvariable=self.hour_shown, values=hour_choice,
                                 width=3, height=5)
        min_menu = ttk.Combobox(self.new_window, textvariable=self.min_shown, values=min_choice,
                                width=3, height=5)
        confirm_button = tk.Button(self.new_window, text="Confirm", font=("times", 20, "bold"),
                                   command=lambda: self.change(self.hour_shown.get(), self.min_shown.get()))

        hour_min_label.place(x=30, y=1)
        hour_menu.place(x=25, y=20)
        min_menu.place(x=85, y=20)
        confirm_button.place(x=250, y=20)

    def switch(self):
        if self.ONorOFF == "OFF":
            self.ONorOFF = "ON"
            self.switchButton.config(text="ON", fg="lime", background="blue")
        else:
            self.ONorOFF = "OFF"
            self.switchButton.config(text="OFF", fg="white", bg="red")

    def is_integer_num(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True

    def change(self, new_hour, new_min):
        new_time = "{}:{}".format(new_hour, new_min)
        if not self.is_integer_num(new_hour):
            messagebox.showerror("ERROR", "Please enter or choose an integer for the hour!")
        elif int(new_hour) > 23 or int(new_hour) < 0:
            messagebox.showerror("ERROR", "The hour should be in between 0 to 23 inclusive!")
        elif not self.is_integer_num(new_min):
            messagebox.showerror("ERROR", "Please enter or choose an integer for the minute!")
        elif int(new_min) > 59 or int(new_min) < 0:
            messagebox.showerror("ERROR", "The minute should be in between 0 to 59 inclusive!")
        else:
            if int(new_hour) < 10:
                new_hour = f"{int(new_hour):02d}"
            if int(new_min) < 10:
                new_min = f"{int(new_min):02d}"
            new_time = "{}:{}".format(new_hour, new_min)
            self.time = new_time
            self.alarmTime.config(text=self.time)
            self.changeButton['state'] = 'normal'
            self.switchButton['state'] = 'normal'
            self.delete_button_cover.destroy()
            if self.ONorOFF == "OFF":
                self.switch()
            self.new_window.destroy()

    def check_time(self):
        if self.ONorOFF == 'ON':
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            alarm_time = f"{self.time}:00"
            if alarm_time == current_time:
                print("Wake UP!")
                time.sleep(1)
                # webbrowser.open('https://www.youtube.com/watch?v=nPdF8J5sIt4', new=1)
                # self.switch()  # Automatically turn off the Alarm.

    def close_new_window_warning(self):
        response = messagebox.askyesno("Not a right way to close the window.", "Do you want to change the time of the "
                                                                               "alarm?")
        if response:
            self.change(self.hour_shown.get(), self.min_shown.get())
        if not response:
            self.changeButton['state'] = 'normal'
            if not self.time[1] == "-":
                self.switchButton['state'] = 'normal'
            self.new_window.destroy()
            self.delete_button_cover.destroy()
