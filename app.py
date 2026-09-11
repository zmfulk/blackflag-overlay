import customtkinter as ctk
import json
import os
import keyboard 

# dark theme to fit ac 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class BlackFlagController(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Black Flag Overlay Controller")
        self.geometry("380x720")
        self.attributes("-topmost", True) 

        # State Variables
        self.deaths = 0
        self.total_seconds = 0
        self.is_running = False
        self.data_file = "data.js"
        self.current_objective = ""
        
        # Checkbox Variables
        self.show_topbar_var = ctk.BooleanVar(value=True)
        self.show_webcam_var = ctk.BooleanVar(value=True)
        self.show_objective_var = ctk.BooleanVar(value=True)

        self.load_data()

        # ----------------------------------- TIMER SECTION -----------------------------------

        # Timer Frame
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Timer Label
        self.timer_label = ctk.CTkLabel(self.timer_frame, text="Time Played", font=("Georgia", 16, "bold"))
        self.timer_label.pack(pady=(10, 0))

        # Timer Display
        self.time_display = ctk.CTkLabel(self.timer_frame, text=self.format_time(self.total_seconds), font=("Courier New", 28, "bold"), text_color="#a61717")
        self.time_display.pack(pady=5)

        # Timer Control Buttons
        self.timer_btn_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        self.timer_btn_frame.pack(pady=(0, 5))

        # Play/Pause Button
        self.play_btn = ctk.CTkButton(self.timer_btn_frame, text="Play / Pause", width=120, command=self.toggle_timer)
        self.play_btn.pack(side="left", padx=5)

        # Reset Button
        self.reset_timer_btn = ctk.CTkButton(self.timer_btn_frame, text="Reset", width=60, fg_color="#750b0b", hover_color="#a61717", command=self.reset_timer)
        self.reset_timer_btn.pack(side="left", padx=5)

        # Timer Manual Input Row
        self.timer_set_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        self.timer_set_frame.pack(pady=(0, 10))

        # Timer Entry and Set Button
        self.timer_entry = ctk.CTkEntry(self.timer_set_frame, placeholder_text="Seconds...", width=100)
        self.timer_entry.pack(side="left", padx=5)

        # Set Time Button
        self.timer_set_btn = ctk.CTkButton(self.timer_set_frame, text="Set Time", width=80, fg_color="#444444", hover_color="#666666", command=self.set_timer_value)
        self.timer_set_btn.pack(side="left", padx=5)


        # ----------------------------------- DEATH SECTION -----------------------------------

        # Death Frame
        self.death_frame = ctk.CTkFrame(self)
        self.death_frame.pack(fill="x", padx=20, pady=10)

        # Death Label
        self.death_label = ctk.CTkLabel(self.death_frame, text="Desynchronizations", font=("Georgia", 16, "bold"))
        self.death_label.pack(pady=(10, 0))

        # Death Display
        self.death_display = ctk.CTkLabel(self.death_frame, text=str(self.deaths), font=("Courier New", 28, "bold"), text_color="#a61717")
        self.death_display.pack(pady=5)

        # Death Control Buttons
        self.death_btn_frame = ctk.CTkFrame(self.death_frame, fg_color="transparent")
        self.death_btn_frame.pack(pady=(0, 5))

        # Add and Remove Death Buttons
        self.minus_btn = ctk.CTkButton(self.death_btn_frame, text="-1", width=50, command=self.remove_death)
        self.minus_btn.pack(side="left", padx=5)
        self.plus_btn = ctk.CTkButton(self.death_btn_frame, text="+1", width=50, command=self.add_death, fg_color="#750b0b", hover_color="#a61717")
        self.plus_btn.pack(side="left", padx=5)

        # Reset Deaths Button
        self.reset_death_btn = ctk.CTkButton(self.death_btn_frame, text="Reset", width=60, fg_color="#750b0b", hover_color="#a61717", command=self.reset_deaths)
        self.reset_death_btn.pack(side="left", padx=5)

        # Deaths Manual Input Row
        self.death_set_frame = ctk.CTkFrame(self.death_frame, fg_color="transparent")
        self.death_set_frame.pack(pady=(0, 10))
        
        self.death_entry = ctk.CTkEntry(self.death_set_frame, placeholder_text="Count...", width=100)
        self.death_entry.pack(side="left", padx=5)

        self.death_set_btn = ctk.CTkButton(self.death_set_frame, text="Set Deaths", width=80, fg_color="#444444", hover_color="#666666", command=self.set_death_value)
        self.death_set_btn.pack(side="left", padx=5)

        # ----------------------------------- OBJECTIVE SECTION -----------------------------------

        # Objective Frame
        self.obj_frame = ctk.CTkFrame(self)
        self.obj_frame.pack(fill="x", padx=20, pady=10)

        # Objective Label and Entry
        self.obj_label = ctk.CTkLabel(self.obj_frame, text="Current Objective", font=("Georgia", 16, "bold"))
        self.obj_label.pack(pady=(10, 0))

        # Objective Entry
        self.obj_entry = ctk.CTkEntry(self.obj_frame, placeholder_text="e.g., Hunting El Impoluto", width=250)
        self.obj_entry.pack(pady=10)

        # Objective Control Buttons
        self.obj_btn_frame = ctk.CTkFrame(self.obj_frame, fg_color="transparent")
        self.obj_btn_frame.pack(pady=(0, 10))

        # Set and Clear Objective Buttons
        self.obj_set_btn = ctk.CTkButton(self.obj_btn_frame, text="Update", width=100, fg_color="#750b0b", hover_color="#a61717", command=self.set_objective)
        self.obj_set_btn.pack(side="left", padx=5)

        self.obj_clear_btn = ctk.CTkButton(self.obj_btn_frame, text="Clear", width=100, fg_color="#444444", hover_color="#666666", command=self.clear_objective)
        self.obj_clear_btn.pack(side="left", padx=5)

        # ----------------------------------- SETTINGS & HOTKEYS SECTION -----------------------------------

        # Settings Frame
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

        self.obj_cb = ctk.CTkCheckBox(self.settings_frame, text="Show Objective", variable=self.show_objective_var, command=self.save_data)
        self.obj_cb.pack(pady=(5, 10))

        # --- GLOBAL HOTKEYS ---
        keyboard.add_hotkey('ctrl+shift+p', lambda: self.after(0, self.toggle_timer))
        keyboard.add_hotkey('ctrl+shift+d', lambda: self.after(0, self.add_death))
        keyboard.add_hotkey('ctrl+shift+x', lambda: self.after(0, self.remove_death))

        # Start the timer loop
        self.update_clock()

    # This function formats the time in seconds to HH:MM:SS format
    def format_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # Toggle the timer's running state
    def toggle_timer(self):
        self.is_running = not self.is_running
        self.save_data()

    # Add a death and update the display
    def add_death(self):
        self.deaths += 1
        self.death_display.configure(text=str(self.deaths))
        self.save_data()

    # Remove a death and update the display
    def remove_death(self):
        if self.deaths > 0:
            self.deaths -= 1
            self.death_display.configure(text=str(self.deaths))
            self.save_data()

    # Set the current objective from the entry field and save it
    def set_objective(self):
        self.current_objective = self.obj_entry.get()
        self.save_data()

    # Clear the current objective and update the display   
    def clear_objective(self):
        self.obj_entry.delete(0, 'end')
        self.current_objective = ""
        self.save_data()

    # Reset the timer and update the display
    def reset_timer(self):
        self.is_running = False
        self.total_seconds = 0
        self.time_display.configure(text=self.format_time(self.total_seconds))
        self.save_data()

    # Reset the death count and update the display
    def reset_deaths(self):
        self.deaths = 0
        self.death_display.configure(text=str(self.deaths))
        self.save_data()

    # Set the timer value from the entry field and update the display
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

    # Set the death count from the entry field and update the display
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

    # updates the timer every second if it's running
    def update_clock(self):
        if self.is_running:
            self.total_seconds += 1
            self.time_display.configure(text=self.format_time(self.total_seconds))
            self.save_data()
        
        self.after(1000, self.update_clock)

    # saves the current state to a JavaScript file for the overlay to read
    def save_data(self):
        data = {
            "deaths": self.deaths,
            "timer_seconds": self.total_seconds,
            "timer_string": self.format_time(self.total_seconds),
            "is_running": self.is_running,
            "current_objective": self.current_objective,
            "show_topbar": self.show_topbar_var.get(),
            "show_webcam": self.show_webcam_var.get(),
            "show_objective": self.show_objective_var.get()
        }
        try:
            with open(self.data_file, "w") as f:
                f.write(f"var overlayData = {json.dumps(data)};")
        except Exception as e:
            print("Error saving data:", e)

    # loads the state from the JavaScript file if it exists
    def load_data(self):

        # Check if the data file exists and load its contents
        if os.path.exists(self.data_file):

            # Read the data file and parse the JSON content
            try:
                with open(self.data_file, "r") as f:

                    # Read the content and remove the JavaScript variable declaration to isolate the JSON string
                    content = f.read()
                    json_str = content.replace("var overlayData = ", "").replace(";", "")
                    data = json.loads(json_str)

                    # Load the state variables from the parsed data
                    self.deaths = data.get("deaths", 0)
                    self.total_seconds = data.get("timer_seconds", 0)
                    self.is_running = data.get("is_running", False)

                    # Update the display labels with the loaded values
                    self.current_objective = data.get("current_objective", "")
                    if self.current_objective:
                        self.obj_entry.insert(0, self.current_objective)
                    
                    # Load visibility preferences
                    self.show_topbar_var.set(data.get("show_topbar", True))
                    self.show_webcam_var.set(data.get("show_webcam", True))
                    self.show_objective_var.set(data.get("show_objective", True))
            except:
                pass

# run it
if __name__ == "__main__":
    app = BlackFlagController()
    app.mainloop()