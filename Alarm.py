import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import time


class Alarm:
    def __init__(self, window, position, time, controller, **kw):
        super().__init__(**kw)

        self.controller = controller
        self.window = window
        self.position = position
        self.time = time
        self.ONorOFF = "OFF"
        self.repeat_options = ['Never', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.repeat_mode = ['Never']
        self.repeat_mode_temp = ['Never']

        self.alarmNumber = tk.Label(self.window, text="Alarm #" + str(self.position + 1), font=("times", 20, "bold"))
        self.alarmTime = tk.Label(self.window, text=self.time, font=("times", 33, "bold"))
        self.nota = tk.Label(window, text="Hours   Minutes", font=("times", 10, "bold"))
        self.changeButton = tk.Button(self.window, text="Setting", font=("times", 20, "bold"),
                                      command=self.changeWindow)
        self.switchButton = tk.Button(self.window, text="OFF", font=("times", 20, "bold"), state='disable',
                                      fg="red", command=self.switch)
        self.repeat_nota = tk.Label(window, text="Repeat", font=("times", 8, "bold"))
        self.repeat_label = tk.Label(window, text="Never", font=("times", 8, "bold"))

        self.alarmNumber.place(x=50, y=(45 + (100 * self.position)))
        self.alarmTime.place(x=30, y=(75 + (100 * self.position)))
        self.nota.place(x=30, y=(120 + (100 * self.position)))
        self.changeButton.place(x=180, y=(80 + (100 * self.position)))
        self.switchButton.place(x=190, y=(50 + 100 * self.position))
        self.repeat_nota.place(x=150, y=(110 + 100 * self.position))
        self.repeat_label.place(x=150, y=(122 + 100 * self.position))

        self.check_time()

    def delete(self):
        if self.time[1] == '-':
            self.delete_alarm()
            return True
        else:
            response = messagebox.askyesno('Deleting', f'Do you want to delete Alarm #{self.position+1}?')
            if response:
                self.delete_alarm()
                return True
            else:
                return False

    def delete_alarm(self):
        self.alarmNumber.place_forget()
        self.alarmTime.place_forget()
        self.nota.place_forget()
        self.changeButton.place_forget()
        self.switchButton.place_forget()
        self.repeat_nota.place_forget()
        self.repeat_label.place_forget()

    def move_up(self):
        self.position -= 1
        self.alarmNumber['text'] = "Alarm #" + str(self.position + 1)
        self.alarmNumber.place(x=50, y=(45 + (100 * self.position)))
        self.alarmTime.place(x=30, y=(75 + (100 * self.position)))
        self.nota.place(x=30, y=(120 + (100 * self.position)))
        self.changeButton.place(x=180, y=(80 + (100 * self.position)))
        self.switchButton.place(x=190, y=(50 + 100 * self.position))
        self.repeat_nota.place(x=150, y=(110 + 100 * self.position))
        self.repeat_label.place(x=150, y=(122 + 100 * self.position))

    def changeWindow(self):
        self.changeButton['state'] = 'disable'
        self.switchButton['state'] = 'disable'

        self.delete_button_cover = tk.Button(self.window, text="X", font=("times", 20, "bold"), fg='red',
                                             state='disable')
        position = "+270+" + str(80 + 100 * self.position)
        self.delete_button_cover.place(x=5, y=(80 + (100 * self.position)))

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
        self.repeat_shown = tk.StringVar(self.new_window)

        hour_min_repeat_label = tk.Label(self.new_window, text="Hours         Minutes      Repeat",
                                         font=("times", 10, "bold"))
        # The state of the hour and minute menu could be "normal" to let the user input the specific time they want.
        # It is code in the Confirming/change method to prevent not working input, such as none integer.
        # The readonly state is to prevent the hacking risk.
        hour_menu = ttk.Combobox(self.new_window, textvariable=self.hour_shown, values=hour_choice,
                                 width=3, height=5, state="normal")
        min_menu = ttk.Combobox(self.new_window, textvariable=self.min_shown, values=min_choice,
                                width=3, height=5, state='normal')
        self.repeat_menu_button = tk.Menubutton(self.new_window, text=self.repeat_mode, indicatoron=True,
                                                relief="raised")
        self.repeat_menu = tk.Menu(self.repeat_menu_button, tearoff=False)
        self.choices = {}
        for choice in self.repeat_options:
            self.choices[choice] = tk.IntVar(value=0)
            self.repeat_menu.add_checkbutton(label=choice, variable=self.choices[choice],
                                             onvalue=1, offvalue=0, command=self.printValues)
        self.repeat_menu_button.config(menu=self.repeat_menu)
        confirm_button = tk.Button(self.new_window, text="Confirm", font=("times", 20, "bold"),
                                   command=lambda: self.change(self.hour_shown.get(), self.min_shown.get()))

        hour_min_repeat_label.place(x=30, y=1)
        hour_menu.place(x=25, y=20)
        min_menu.place(x=85, y=20)
        self.repeat_menu_button.place(x=145, y=20)
        confirm_button.place(x=270, y=20)

    def printValues(self):
        if self.choices['Never'].get() == 1 and 'Never' not in self.repeat_mode_temp:
            for day, var in self.choices.items():
                if var.get() == 1 and not day == 'Never':
                    self.choices[day].set(0)
        else:
            self.choices['Never'].set(0)
        chosen_day = []
        for day, var in self.choices.items():
            if var.get() == 1:
                chosen_day.append(day)
        self.repeat_mode_temp = chosen_day
        self.repeat_menu_button.config(text=chosen_day)

    def switch(self):
        if self.ONorOFF == "OFF":
            self.ONorOFF = "ON"
            self.switchButton.config(text="ON", fg="lime", padx=5)
        else:
            self.ONorOFF = "OFF"
            self.switchButton.config(text="OFF", fg="red", padx=0)

    def is_integer_num(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True

    def duplicated_alarm(self, new_time):
        var = self.controller.show_time(self.position)
        if new_time in var:
            return True
        else:
            return False

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
        elif self.duplicated_alarm(new_time):
            messagebox.showerror("ERROR", "Please do not have two alarm the same time.")
        else:
            if int(new_hour) < 10:
                new_hour = f"{int(new_hour):02d}"
            if int(new_min) < 10:
                new_min = f"{int(new_min):02d}"
            new_time = "{}:{}".format(new_hour, new_min)
            self.time = new_time
            self.alarmTime.config(text=self.time)
            self.repeat_mode = self.repeat_mode_temp
            if self.repeat_mode == ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
                self.repeat_label.config(text='Weekdays')
            elif self.repeat_mode == ['Sun', 'Sat']:
                self.repeat_label.config(text='Weekends')
            elif self.repeat_mode == ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
                self.repeat_label.config(text='Everyday')
            else:
                self.repeat_label.config(text=self.repeat_mode)
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
            current_day = now.strftime("%a")
            alarm_time = f"{self.time}:00"
            if alarm_time == current_time and current_day in self.repeat_mode:
                print("Wake UP!")
                time.sleep(1)
            elif self.repeat_mode == ['Never'] and alarm_time == current_time:
                print("Wake UP!")
                time.sleep(1)
                self.switch()
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
