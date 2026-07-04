import customtkinter as ctk
import json
import os
import keyboard 

# Set up the theme to match the dark aesthetic
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class BlackFlagController(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Black Flag Overlay Controller")
        self.geometry("380x620") # Increased height for the settings section
        self.attributes("-topmost", True) 

        # State Variables
        self.deaths = 0
        self.total_seconds = 0
        self.is_running = False
        self.data_file = "data.js"
        
        # Checkbox Variables
        self.show_topbar_var = ctk.BooleanVar(value=True)
        self.show_webcam_var = ctk.BooleanVar(value=True)

        self.load_data()

        # --- TIMER SECTION ---
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.timer_label = ctk.CTkLabel(self.timer_frame, text="Time Played", font=("Georgia", 16, "bold"))
        self.timer_label.pack(pady=(10, 0))

        self.time_display = ctk.CTkLabel(self.timer_frame, text=self.format_time(self.total_seconds), font=("Courier New", 28, "bold"), text_color="#a61717")
        self.time_display.pack(pady=5)

        self.timer_btn_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        self.timer_btn_frame.pack(pady=(0, 5))

        self.play_btn = ctk.CTkButton(self.timer_btn_frame, text="Play / Pause", width=120, command=self.toggle_timer)
        self.play_btn.pack(side="left", padx=5)
        
        self.reset_timer_btn = ctk.CTkButton(self.timer_btn_frame, text="Reset", width=60, fg_color="#750b0b", hover_color="#a61717", command=self.reset_timer)
        self.reset_timer_btn.pack(side="left", padx=5)

        # Timer Manual Input Row
        self.timer_set_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        self.timer_set_frame.pack(pady=(0, 10))
        
        self.timer_entry = ctk.CTkEntry(self.timer_set_frame, placeholder_text="Seconds...", width=100)
        self.timer_entry.pack(side="left", padx=5)
        
        self.timer_set_btn = ctk.CTkButton(self.timer_set_frame, text="Set Time", width=80, fg_color="#444444", hover_color="#666666", command=self.set_timer_value)
        self.timer_set_btn.pack(side="left", padx=5)


        # --- DEATHS SECTION ---
        self.death_frame = ctk.CTkFrame(self)
        self.death_frame.pack(fill="x", padx=20, pady=10)

        self.death_label = ctk.CTkLabel(self.death_frame, text="Desynchronizations", font=("Georgia", 16, "bold"))
        self.death_label.pack(pady=(10, 0))

        self.death_display = ctk.CTkLabel(self.death_frame, text=str(self.deaths), font=("Courier New", 28, "bold"), text_color="#a61717")
        self.death_display.pack(pady=5)

        self.death_btn_frame = ctk.CTkFrame(self.death_frame, fg_color="transparent")
        self.death_btn_frame.pack(pady=(0, 5))

        self.minus_btn = ctk.CTkButton(self.death_btn_frame, text="-1", width=50, command=self.remove_death)
        self.minus_btn.pack(side="left", padx=5)

        self.plus_btn = ctk.CTkButton(self.death_btn_frame, text="+1", width=50, command=self.add_death, fg_color="#750b0b", hover_color="#a61717")
        self.plus_btn.pack(side="left", padx=5)
        
        self.reset_death_btn = ctk.CTkButton(self.death_btn_frame, text="Reset", width=60, fg_color="#750b0b", hover_color="#a61717", command=self.reset_deaths)
        self.reset_death_btn.pack(side="left", padx=5)

        # Deaths Manual Input Row
        self.death_set_frame = ctk.CTkFrame(self.death_frame, fg_color="transparent")
        self.death_set_frame.pack(pady=(0, 10))
        
        self.death_entry = ctk.CTkEntry(self.death_set_frame, placeholder_text="Count...", width=100)
        self.death_entry.pack(side="left", padx=5)
        
        self.death_set_btn = ctk.CTkButton(self.death_set_frame, text="Set Deaths", width=80, fg_color="#444444", hover_color="#666666", command=self.set_death_value)
        self.death_set_btn.pack(side="left", padx=5)

        # --- SETTINGS & HOTKEYS SECTION ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(fill="x", padx=20, pady=10)

        self.settings_label = ctk.CTkLabel(self.settings_frame, text="Settings & Hotkeys", font=("Georgia", 14, "bold"))
        self.settings_label.pack(pady=(10, 0))

        # Hotkeys Text
        hotkeys_text = "Play/Pause: Ctrl + Shift + P\n+1 Death: Ctrl + Shift + D\n-1 Death: Ctrl + Shift + X"
        self.hotkeys_label = ctk.CTkLabel(self.settings_frame, text=hotkeys_text, font=("Arial", 12), text_color="#aaaaaa", justify="center")
        self.hotkeys_label.pack(pady=5)

        # Checkboxes
        self.checkbox_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.checkbox_frame.pack(pady=(5, 10))

        self.topbar_cb = ctk.CTkCheckBox(self.checkbox_frame, text="Show Stats Bar", variable=self.show_topbar_var, command=self.save_data)
        self.topbar_cb.pack(side="left", padx=10)

        self.webcam_cb = ctk.CTkCheckBox(self.checkbox_frame, text="Show Webcam Frame", variable=self.show_webcam_var, command=self.save_data)
        self.webcam_cb.pack(side="left", padx=10)

        # --- GLOBAL HOTKEYS ---
        keyboard.add_hotkey('ctrl+shift+p', lambda: self.after(0, self.toggle_timer))
        keyboard.add_hotkey('ctrl+shift+d', lambda: self.after(0, self.add_death))
        keyboard.add_hotkey('ctrl+shift+x', lambda: self.after(0, self.remove_death))

        # Start the timer loop
        self.update_clock()

    def format_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.save_data()

    def add_death(self):
        self.deaths += 1
        self.death_display.configure(text=str(self.deaths))
        self.save_data()

    def remove_death(self):
        if self.deaths > 0:
            self.deaths -= 1
            self.death_display.configure(text=str(self.deaths))
            self.save_data()

    def reset_timer(self):
        self.is_running = False
        self.total_seconds = 0
        self.time_display.configure(text=self.format_time(self.total_seconds))
        self.save_data()

    def reset_deaths(self):
        self.deaths = 0
        self.death_display.configure(text=str(self.deaths))
        self.save_data()

    def set_timer_value(self):
        try:
            val = int(self.timer_entry.get())
            if val >= 0:
                self.total_seconds = val
                self.time_display.configure(text=self.format_time(self.total_seconds))
                self.save_data()
            self.timer_entry.delete(0, 'end')
        except ValueError:
            self.timer_entry.delete(0, 'end')

    def set_death_value(self):
        try:
            val = int(self.death_entry.get())
            if val >= 0:
                self.deaths = val
                self.death_display.configure(text=str(self.deaths))
                self.save_data()
            self.death_entry.delete(0, 'end')
        except ValueError:
            self.death_entry.delete(0, 'end')

    def update_clock(self):
        if self.is_running:
            self.total_seconds += 1
            self.time_display.configure(text=self.format_time(self.total_seconds))
            self.save_data()
        
        self.after(1000, self.update_clock)

    def save_data(self):
        data = {
            "deaths": self.deaths,
            "timer_seconds": self.total_seconds,
            "timer_string": self.format_time(self.total_seconds),
            "is_running": self.is_running,
            "show_topbar": self.show_topbar_var.get(),
            "show_webcam": self.show_webcam_var.get()
        }
        try:
            with open(self.data_file, "w") as f:
                f.write(f"var overlayData = {json.dumps(data)};")
        except Exception as e:
            print("Error saving data:", e)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    content = f.read()
                    json_str = content.replace("var overlayData = ", "").replace(";", "")
                    data = json.loads(json_str)
                    
                    self.deaths = data.get("deaths", 0)
                    self.total_seconds = data.get("timer_seconds", 0)
                    self.is_running = False
                    
                    # Load visibility preferences
                    self.show_topbar_var.set(data.get("show_topbar", True))
                    self.show_webcam_var.set(data.get("show_webcam", True))
            except:
                pass

if __name__ == "__main__":
    app = BlackFlagController()
    app.mainloop()