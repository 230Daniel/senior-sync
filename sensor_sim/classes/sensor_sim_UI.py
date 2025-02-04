import customtkinter as ctk
from .mock_sensor_manager import MockSensorManager

class SensorSimUI:
    def __init__(self, root):
        # Start Sensor Manager
        self.manager = MockSensorManager()

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

        if self.sensor_count > 0:
            self.update_sensor_values()

    def add_sensor(self):
        """Adds a new sensor row to the UI."""

        colour_status_boundaries = []

        popup = ctk.CTkToplevel()
        popup.title("Add New Sensor")
        popup.geometry("300x200")

        popup.columnconfigure(1, weight=1)

        ctk.CTkLabel(popup, text="Sensor ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        sensor_id_entry = ctk.CTkEntry(popup)
        sensor_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(popup, text="Friendly Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        friendly_name_entry = ctk.CTkEntry(popup)
        friendly_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(popup, text="Unit:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        unit_entry = ctk.CTkEntry(popup)
        unit_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(popup, text="Value Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        value_type_menu = ctk.CTkOptionMenu(popup, values=["int", "float", "str"])
        value_type_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        threshold_frame = ctk.CTkFrame(popup)
        threshold_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        threshold_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(threshold_frame, text="Threshold:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        threshold_entry = ctk.CTkEntry(threshold_frame)
        threshold_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(threshold_frame, text="Colour:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        colour_menu = ctk.CTkOptionMenu(threshold_frame, values=["red", "amber", "green"])
        colour_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        limits_frame = ctk.CTkFrame(popup)
        limits_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        limits_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(limits_frame, text="Normal Limits").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(limits_frame, text="Min:").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        normal_limits_min_entry = ctk.CTkEntry(limits_frame)
        normal_limits_min_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(limits_frame, text="Max:").grid(row=0, column=3, padx=10, pady=5, sticky="e")
        normal_limits_max_entry = ctk.CTkEntry(limits_frame)
        normal_limits_max_entry.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(limits_frame, text="Dangerous Limits").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(limits_frame, text="Min:").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        dangerous_limits_min_entry = ctk.CTkEntry(limits_frame)
        dangerous_limits_min_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(limits_frame, text="Max:").grid(row=1, column=3, padx=10, pady=5, sticky="e")
        dangerous_limits_max_entry = ctk.CTkEntry(limits_frame)
        dangerous_limits_max_entry.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(limits_frame, text="Deadly Limits").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(limits_frame, text="Min:").grid(row=2, column=1, padx=10, pady=5, sticky="e")
        deadly_limits_min_entry = ctk.CTkEntry(limits_frame)
        deadly_limits_min_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(limits_frame, text="Max:").grid(row=2, column=3, padx=10, pady=5, sticky="e")
        deadly_limits_max_entry = ctk.CTkEntry(limits_frame)
        deadly_limits_max_entry.grid(row=2, column=4, padx=10, pady=5, sticky="ew")
    
        def add_threshold():
            colour_status_boundary = {
                "threshold": threshold_entry.get(),
                "colour": colour_menu.get()
            }
            colour_status_boundaries.append(colour_status_boundary)

        def submit():
            self.manager.add_sensor(id=sensor_id_entry.get(),
                                    friendly_name=friendly_name_entry.get(),
                                    unit=unit_entry.get(),
                                    value_type=value_type_menu.get(),
                                    colour_status_boundaries= colour_status_boundaries,
                                    normal_limits={"min": int(normal_limits_min_entry.get()),"max": int(normal_limits_max_entry.get())},
                                    dangerous_limits={"min": int(dangerous_limits_min_entry.get()),"max": int(dangerous_limits_max_entry.get())},
                                    deadly_limits={"min": int(deadly_limits_min_entry.get()),"max": int(deadly_limits_max_entry.get())})

            self.sensor_count += 1
            colour_status_boundaries.clear()

            # Sensor name label
            sensor_label = ctk.CTkLabel(self.scrollable_frame, text=f"{friendly_name_entry.get()}", font=("Arial", 10))
            sensor_label.grid(row=self.sensor_count, column=0, padx=20, sticky="w")

            # Sensor value label
            value_label = ctk.CTkLabel(self.scrollable_frame, text="--", font=("Arial", 10))
            value_label.grid(row=self.sensor_count, column=1, padx=20, sticky="w")

            def update_sensor_mode(new_mode, index):
                sensor_id = self.manager.sensors[index-2].id
                self.manager.switch_sensor_mode(id=sensor_id, mode=new_mode)

            # Sensor mode dropdown
            mode_combo = ctk.CTkOptionMenu(self.scrollable_frame, values=["normal", "dangerous", "deadly"], state="readonly")
            mode_combo.set("normal")
            mode_combo.configure(command=lambda new_mode, index=self.sensor_count: update_sensor_mode(new_mode, index))
            mode_combo.grid(row=self.sensor_count, column=2, padx=20)

            # Ensure the canvas updates its scrollregion
            self.sensor_canvas.update_idletasks()
            # popup.destroy() # TODO: uncomment when done
        
        add_threshold_button = ctk.CTkButton(threshold_frame, text="Add Threshold", command=add_threshold)
        add_threshold_button.grid(row=2, column=1, padx=5, pady=5)

        add_sensor_button = ctk.CTkButton(popup, text="Add Sensor", command=submit)
        add_sensor_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.root.update_idletasks()  # Update all widgets to calculate size
        popup_height = popup.winfo_reqheight() + 20  # Add vertical padding
        popup.geometry(f"600x{popup_height}")
    
    def update_sensor_values(self):
            sensor_values = self.manager.get_sensor_values()
            for row, sensor in enumerate(sensor_values, start=1):
                self.scrollable_frame.grid_slaves(row=row+1, column=1)[0].configure(text=f"{sensor["value"]}")

            # Refresh every second
            self.root.after(1000, self.update_sensor_values)


