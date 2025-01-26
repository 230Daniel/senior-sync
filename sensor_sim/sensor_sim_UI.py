import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class SensorSimUI:
    def __init__(self, root):
        self.sensor_count = 1

        self.root = root
        self.root.title("Mock Sensor UI")
        self.root.geometry("700x400")  # Fixed window size
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)  # Entire column for content
        ctk.set_appearance_mode("System")  # Light/Dark mode based on system
        ctk.set_default_color_theme("blue")  # Default theme
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]

        # Calculate and set dynamic geometry with a border
        self.root.update_idletasks()  # Update all widgets to calculate size
        # window_width = root.winfo_reqwidth() + 20  # Add horizontal padding
        # self.window_height = self.root.winfo_reqheight() + 20  # Add vertical padding
        # self.root.geometry(f"{700}x{500}")
        self.root.resizable(False, False)

        # Header
        self.header_frame = ctk.CTkFrame(root)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)  # Expand title label
        self.header_frame.grid_columnconfigure(3, weight=0)  # Keep button tight
        self.title = ctk.CTkLabel(self.header_frame, text="Mock Sensor UI", font=("Arial", 16))
        self.title.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="w")

        # Add sensor button
        self.add_sensor_btn = ctk.CTkButton(self.header_frame, text="+ Add new sensor", font=("Arial", 10), command=self.add_sensor)
        self.add_sensor_btn.grid(row=0, column=3, padx=20, sticky="ew")

        # Sensor List
        self.sensor_list_frame = ctk.CTkFrame(root)
        self.sensor_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.sensor_list_frame.grid_columnconfigure(0, weight=1)

        # Scrollable canvas containing all sensors
        self.sensor_canvas = ctk.CTkCanvas(self.sensor_list_frame, bg=bg_color, highlightthickness=0)
        self.sensor_canvas.grid_columnconfigure(0, weight=1)
        self.scrollbar = ctk.CTkScrollbar(root, command=self.sensor_canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.sensor_canvas)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        # Bind the scrollable_frame width to match the canvas width
        self.sensor_canvas.bind(
            "<Configure>",
            lambda e: self.sensor_canvas.itemconfig(self.canvas_window, width=e.width)
        )

        # Create the window within the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sensor_canvas.configure(scrollregion=self.sensor_canvas.bbox("all"))
        )

        self.canvas_window = self.sensor_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.sensor_canvas.configure(yscrollcommand=self.scrollbar.set)


        self.sensor_canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.scrollbar.grid_columnconfigure(1, weight=1)

        # Column headers
        self.sensor_label = ctk.CTkLabel(self.scrollable_frame, text="Sensor", font=("Arial", 12, "bold"))
        self.sensor_label.grid(row=0, column=0, padx=20, sticky="w")

        self.value_label = ctk.CTkLabel(self.scrollable_frame, text="Value", font=("Arial", 12, "bold"))
        self.value_label.grid(row=0, column=1, padx=20, sticky="w")

        self.mode_label = ctk.CTkLabel(self.scrollable_frame, text="Mode", font=("Arial", 12, "bold"))
        self.mode_label.grid(row=0, column=2, padx=20)

    def add_sensor(self):
        print("Add new sensor button clicked")
        """Adds a new sensor row to the UI."""
        self.sensor_count += 1

        # Create a frame for the new sensor row
        # sensor_frame = ctk.CTkFrame(self.scrollable_frame)
        # sensor_frame.grid(row=self.sensor_count, column=0, sticky="nsew", padx=10, pady=5)
        # sensor_frame.grid_columnconfigure(0, weight=1)
        # sensor_frame.grid_columnconfigure(1, weight=1)
        # sensor_frame.grid_columnconfigure(2, weight=1)

        # Sensor name label
        sensor_label = ctk.CTkLabel(self.scrollable_frame, text=f"Sensor {self.sensor_count}", font=("Arial", 10))
        sensor_label.grid(row=self.sensor_count, column=0, padx=20, sticky="w")

        # Sensor value label
        value_label = ctk.CTkLabel(self.scrollable_frame, text="--", font=("Arial", 10))
        value_label.grid(row=self.sensor_count, column=1, padx=20, sticky="w")

        # Sensor mode dropdown
        mode_combo = ctk.CTkOptionMenu(self.scrollable_frame, values=["Normal", "Dangerous"], state="readonly")
        mode_combo.set("Normal")
        mode_combo.grid(row=self.sensor_count, column=2, padx=20)

        # Ensure the canvas updates its scrollregion
        self.sensor_canvas.update_idletasks()

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = SensorSimUI(root)
    root.mainloop()
