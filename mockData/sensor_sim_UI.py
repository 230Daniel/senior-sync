import tkinter as tk
from tkinter import ttk

sensor_count = 0

# Function to handle the "Add new sensor" button
def add_sensor():
    print("Add new sensor button clicked")
    """Adds a new sensor row to the UI."""
    sensor_count += 1

    # Create a frame for the new sensor row
    sensor_frame = tk.Frame(scrollable_frame)
    sensor_frame.grid(row=sensor_count, column=0, sticky="ew", padx=10, pady=5)

    # Sensor name label
    sensor_label = tk.Label(sensor_frame, text=f"Sensor {self.sensor_count}", font=("Arial", 10))
    sensor_label.grid(row=0, column=0, padx=10, sticky="w")

    # Sensor value label
    value_label = tk.Label(sensor_frame, text="--", font=("Arial", 10))
    value_label.grid(row=0, column=1, padx=20)

    # Sensor mode dropdown
    mode_combo = ttk.Combobox(sensor_frame, values=["Normal", "Dangerous"], state="readonly")
    mode_combo.set("Normal")
    mode_combo.grid(row=0, column=2, padx=20)

    # Ensure the canvas updates its scrollregion
    self.sensor_canvas.update_idletasks()

# Root window
root = tk.Tk()
root.title("Mock Sensor UI")
root.grid_columnconfigure(0, weight=1)

# Header
header_frame = tk.Frame(root)
header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
header_frame.grid_columnconfigure(0, weight=1)  # Expand title label
header_frame.grid_columnconfigure(1, weight=0)  # Keep button tight
title = tk.Label(header_frame, text="Mock Sensor UI", font=("Arial", 16))
title.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="w")

# Add sensor button
add_sensor_btn = tk.Button(header_frame, text="+ Add new sensor", bg="purple", fg="white", font=("Arial", 10), command=add_sensor)
add_sensor_btn.grid(row=0, column=3, padx=20, sticky="ew")

# Sensor List
sensor_list_frame = tk.Frame(root)
sensor_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
sensor_list_frame.grid_columnconfigure(0, weight=1)

# Column headers
column_headers_frame = tk.Frame(sensor_list_frame)
column_headers_frame.grid(row=0, column=0, pady=5, sticky="ew")
column_headers_frame.grid_columnconfigure(0, weight=1)
column_headers_frame.grid_columnconfigure(1, weight=1)
column_headers_frame.grid_columnconfigure(2, weight=1)

sensor_label = tk.Label(column_headers_frame, text="Sensor", font=("Arial", 12, "bold"))
sensor_label.grid(row=0, column=0, padx=10, sticky="ew")

value_label = tk.Label(column_headers_frame, text="Value", font=("Arial", 12, "bold"))
value_label.grid(row=0, column=1, padx=10, sticky="ew")

mode_label = tk.Label(column_headers_frame, text="Mode", font=("Arial", 12, "bold"))
mode_label.grid(row=0, column=2, padx=(200,10), sticky="ew")

# Scrollable canvas containing all sensors
sensor_canvas = tk.Canvas(sensor_list_frame)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=sensor_canvas.yview)
scrollable_frame = tk.Frame(sensor_canvas)

# Create the window within the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: sensor_canvas.configure(scrollregion=sensor_canvas.bbox("all"))
)

sensor_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
sensor_canvas.configure(yscrollcommand=scrollbar.set)


sensor_canvas.grid(row=1, column=0, sticky="nsew")
scrollbar.grid(row=1, column=1, sticky="ns")


# # Row 1: Heart Rate
# sensor_1_label = tk.Label(sensor_list_frame, text="Heart Rate", font=("Arial", 10))
# sensor_1_label.grid(row=1, column=0, pady=5, sticky="ew")

# value_1_label = tk.Label(sensor_list_frame, text="62bpm", font=("Arial", 10))
# value_1_label.grid(row=1, column=1, pady=5, sticky="ew")

# mode_1_combo = ttk.Combobox(sensor_list_frame, values=["Normal", "Dangerous"], state="readonly")
# mode_1_combo.set("Normal")
# mode_1_combo.grid(row=1, column=2, pady=5, sticky="ew")

# # Row 2: O2
# sensor_2_label = tk.Label(sensor_list_frame, text="O2", font=("Arial", 10))
# sensor_2_label.grid(row=2, column=0, pady=5, sticky="ew")

# value_2_label = tk.Label(sensor_list_frame, text="95%", font=("Arial", 10))
# value_2_label.grid(row=2, column=1, pady=5, sticky="ew")

# mode_2_combo = ttk.Combobox(sensor_list_frame, values=["Normal", "Dangerous"], state="readonly")
# mode_2_combo.set("Dangerous")
# mode_2_combo.grid(row=2, column=2, pady=5, sticky="ew")

# Calculate and set dynamic geometry with a border
root.update_idletasks()  # Update all widgets to calculate size
window_width = root.winfo_reqwidth() + 20  # Add horizontal padding
window_height = root.winfo_reqheight() + 20  # Add vertical padding
root.geometry(f"{700}x{window_height}")
root.resizable(False, False)

# Run the application
root.mainloop()
