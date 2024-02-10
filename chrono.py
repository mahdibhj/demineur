import tkinter as tk

class Chronometre:
    def __init__(self, parent):
        self.parent = parent
        self.time = 0
        self.is_running = False
        self.label = tk.Label(self.parent, text="00:00:00", font=("Arial", 24))
        self.label.pack()
        self.button = tk.Button(self.parent, text="Commencer", command=self.toggle)
        self.button.pack()

    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.button.config(text="Pause")
            self.update()
        else:
            self.button.config(text="Commencer")

    def update(self):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.label.config(text=time_str)
        if self.is_running:
            self.parent.after(1000, self.update)
