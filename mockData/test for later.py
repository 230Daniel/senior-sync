import tkinter as tk
from tkinter import ttk

class SensorUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mock Sensor UI")
        self.root.geometry("700x400")  # Fixed window size
        self.root.resizable(False, False)

        # Main layout
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)

        self.sensor_canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.sensor_canvas.yview)
        self.scrollable_frame = tk.Frame(self.sensor_canvas)

        # Create the window within the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sensor_canvas.configure(scrollregion=self.sensor_canvas.bbox("all"))
        )

        self.sensor_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.sensor_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.sensor_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add header
        self.title_label = tk.Label(self.header_frame, text="Mock Sensor UI", font=("Arial", 16))
        self.title_label.pack(side=tk.LEFT)

        self.add_sensor_btn = tk.Button(
            self.header_frame,
            text="+ Add new sensor",
            bg="purple",
            fg="white",
            font=("Arial", 10),
            command=self.add_sensor,
        )
        self.add_sensor_btn.pack(side=tk.RIGHT)

        # Placeholder for sensor data
        self.sensor_count = 0  # Keeps track of the number of sensors

    def add_sensor(self):
        """Adds a new sensor row to the UI."""
        self.sensor_count += 1

        # Create a frame for the new sensor row
        sensor_frame = tk.Frame(self.scrollable_frame, pady=5)
        sensor_frame.pack(fill=tk.X, padx=10, pady=5)

        # Sensor name label
        sensor_label = tk.Label(sensor_frame, text=f"Sensor {self.sensor_count}", font=("Arial", 10))
        sensor_label.pack(side=tk.LEFT, padx=10)

        # Sensor value label
        value_label = tk.Label(sensor_frame, text="--", font=("Arial", 10))
        value_label.pack(side=tk.LEFT, padx=20)

        # Sensor mode dropdown
        mode_combo = ttk.Combobox(sensor_frame, values=["Normal", "Dangerous"], state="readonly")
        mode_combo.set("Normal")
        mode_combo.pack(side=tk.LEFT, padx=20)

        # Ensure the canvas updates its scrollregion
        self.sensor_canvas.update_idletasks()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SensorUIApp(root)
    root.mainloop()
