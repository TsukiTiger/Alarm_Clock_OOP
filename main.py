import time
import tkinter as tk
from tkinter import messagebox
from Alarm import Alarm
import datetime


class AlarmClockApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True

        self.geometry("270x400")
        self.title("Alarm Clock")
        self.resizable(False, False)
        self.alarm_amount = 0

        self.alarm0_time = '--:--'
        self.alarm1_time = '--:--'
        self.alarm2_time = '--:--'

        self.local_time = datetime.datetime.now()
        self.local_timezone = self.local_time.astimezone().tzinfo

        self.current_time = self.local_time.strftime("%H:%M:%S")

        self.current_time_label = tk.Label(self, text=f"Current Time:                  Timezone: {self.local_timezone}",
                                           font=("times", 10, "bold"), bg='green')
        self.current_time_clock = tk.Label(self, text=self.current_time, font=("times", 10, "bold"), bg='green')
        self.add_button = tk.Button(self, text='Add New Alarm', font=("times", 20, "bold"),
                                    command=self.add_alarm)
        self.delete_button0 = tk.Button(self, text="X", font=("times", 20, "bold"), fg='red', state='disable',
                                        command=lambda: self.delete_alarm(0))
        self.delete_button1 = tk.Button(self, text="X", font=("times", 20, "bold"), fg='red', state='disable',
                                        command=lambda: self.delete_alarm(1))
        self.delete_button2 = tk.Button(self, text="X", font=("times", 20, "bold"), fg='red', state='disable',
                                        command=lambda: self.delete_alarm(2))

        self.add_button.place(x=30, y=350)
        self.delete_button0.place(x=5, y=80)
        self.delete_button1.place(x=5, y=180)
        self.delete_button2.place(x=5, y=280)
        self.current_time_clock.place(x=78, y=2)
        self.current_time_label.place(x=5, y=2)

    def show_time(self, calling_position):
        time_exist = [self.alarm0_time, self.alarm1_time, self.alarm2_time]
        del time_exist[calling_position]
        return time_exist

    def check_time(self):
        self.local_time = datetime.datetime.now()
        current_time = self.local_time.strftime("%H:%M:%S")
        self.current_time_clock['text'] = current_time
        if self.alarm_amount == 0:
            pass
        elif self.alarm_amount == 1:
            self.alarm0.check_time()
            self.alarm0_time = self.alarm0.time
            self.alarm1_time = '--:--'
            self.alarm2_time = '--:--'
        elif self.alarm_amount == 2:
            self.alarm0.check_time()
            self.alarm1.check_time()
            self.alarm0_time = self.alarm0.time
            self.alarm1_time = self.alarm1_time
            self.alarm2_time = '--:--'
        else:
            self.alarm0_time = self.alarm0.time
            self.alarm1_time = self.alarm1.time
            self.alarm2_time = self.alarm2.time
            self.alarm0.check_time()
            self.alarm1.check_time()
            self.alarm2.check_time()

    def delete_alarm(self, place):
        if place == 2:
            if self.alarm2.delete():
                self.delete_button2['state'] = 'disable'
                self.alarm_amount -= 1
        elif place == 1:
            if self.alarm_amount == 3:
                if self.alarm1.delete():
                    self.alarm2.move_up()
                    self.alarm1 = self.alarm2
                    self.delete_button2['state'] = 'disable'
                    self.alarm_amount -= 1
            else:
                if self.alarm1.delete():
                    self.delete_button1['state'] = 'disable'
                    self.alarm_amount -= 1
        elif place == 0:
            if self.alarm_amount == 3:
                if self.alarm0.delete():
                    self.alarm1.move_up()
                    self.alarm2.move_up()
                    self.alarm0 = self.alarm1
                    self.alarm1 = self.alarm2
                    self.delete_button2['state'] = 'disable'
                    self.alarm_amount -= 1
            elif self.alarm_amount == 2:
                if self.alarm0.delete():
                    self.alarm1.move_up()
                    self.alarm0 = self.alarm1
                    self.delete_button1['state'] = 'disable'
                    self.alarm_amount -= 1
            else:
                if self.alarm0.delete():
                    self.delete_button0['state'] = 'disable'
                    self.alarm_amount -= 1
        self.add_button['state'] = 'normal'

    def add_alarm(self):
        position = self.alarm_amount
        if self.alarm_amount == 0:
            self.alarm0 = Alarm(self, position, "--:--", self)
            self.delete_button0['state'] = 'normal'
            self.alarm_amount += 1
        elif self.alarm_amount == 1:
            self.alarm1 = Alarm(self, position, "--:--", self)
            self.delete_button1['state'] = 'normal'
            self.alarm_amount += 1
        else:
            self.alarm2 = Alarm(self, position, "--:--", self)
            self.delete_button2['state'] = 'normal'
            self.alarm_amount += 1
            self.add_button['state'] = 'disable'

    def run(self):
        while self.running:
            root.check_time()
            root.update_idletasks()
            root.update()
            time.sleep(0.1)

    def safe_quit(self):
        self.running = False
        response = messagebox.askyesno("Quitting", "Do you want to leave this program?")
        if response:
            self.destroy()
        else:
            self.running = True


if __name__ == '__main__':
    root = AlarmClockApp()
    root.protocol("WM_DELETE_WINDOW", root.safe_quit)
    root.run()
