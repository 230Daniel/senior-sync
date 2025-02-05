import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
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
        self.threshold_frame = None
        self.colour_status_boundaries = []
        self.normal_value_entry = None
        self.dangerous_value_entry = None
        self.deadly_value_entry = None
        self.normal_limits_min_entry = None
        self.normal_limits_max_entry = None
        self.dangerous_limits_min_entry = None
        self.dangerous_limits_max_entry = None
        self.deadly_limits_min_entry = None
        self.deadly_limits_max_entry = None

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

        self.colour_status_boundaries = []

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
        
        def show_input_menu_type(value_type):
            limits_frame = ctk.CTkFrame(popup)
            limits_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            limits_frame.columnconfigure(1, weight=1)

            if value_type == "int" or value_type == "float":
                def add_threshold():
                    colour_status_boundary = {
                        "threshold": threshold_entry.get(),
                        "colour": colour_menu.get()
                    }
                    self.colour_status_boundaries.append(colour_status_boundary)

                self.threshold_frame = ctk.CTkFrame(popup)
                self.threshold_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
                self.threshold_frame.columnconfigure(1, weight=1)

                ctk.CTkLabel(self.threshold_frame, text="Threshold:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                threshold_entry = ctk.CTkEntry(self.threshold_frame)
                threshold_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

                ctk.CTkLabel(self.threshold_frame, text="Colour:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
                colour_menu = ctk.CTkOptionMenu(self.threshold_frame, values=["red", "amber", "green"])
                colour_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

                add_threshold_button = ctk.CTkButton(self.threshold_frame, text="Add Threshold", command=add_threshold)
                add_threshold_button.grid(row=2, column=1, padx=5, pady=5)

                ctk.CTkLabel(limits_frame, text="Normal Limits").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                ctk.CTkLabel(limits_frame, text="Min:").grid(row=0, column=1, padx=10, pady=5, sticky="e")
                self.normal_limits_min_entry = ctk.CTkEntry(limits_frame)
                self.normal_limits_min_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
                ctk.CTkLabel(limits_frame, text="Max:").grid(row=0, column=3, padx=10, pady=5, sticky="e")
                self.normal_limits_max_entry = ctk.CTkEntry(limits_frame)
                self.normal_limits_max_entry.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

                ctk.CTkLabel(limits_frame, text="Dangerous Limits").grid(row=1, column=0, padx=10, pady=5, sticky="e")
                ctk.CTkLabel(limits_frame, text="Min:").grid(row=1, column=1, padx=10, pady=5, sticky="e")
                self.dangerous_limits_min_entry = ctk.CTkEntry(limits_frame)
                self.dangerous_limits_min_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
                ctk.CTkLabel(limits_frame, text="Max:").grid(row=1, column=3, padx=10, pady=5, sticky="e")
                self.dangerous_limits_max_entry = ctk.CTkEntry(limits_frame)
                self.dangerous_limits_max_entry.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

                ctk.CTkLabel(limits_frame, text="Deadly Limits").grid(row=2, column=0, padx=10, pady=5, sticky="e")
                ctk.CTkLabel(limits_frame, text="Min:").grid(row=2, column=1, padx=10, pady=5, sticky="e")
                self.deadly_limits_min_entry = ctk.CTkEntry(limits_frame)
                self.deadly_limits_min_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
                ctk.CTkLabel(limits_frame, text="Max:").grid(row=2, column=3, padx=10, pady=5, sticky="e")
                self.deadly_limits_max_entry = ctk.CTkEntry(limits_frame)
                self.deadly_limits_max_entry.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

            if value_type == "str":
                try:
                    self.threshold_frame.grid_forget()
                except:
                    print("cant remove threshold frame. doesn;'t exist")
                    pass

                ctk.CTkLabel(limits_frame, text="Normal Value").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                self.normal_value_entry = ctk.CTkEntry(limits_frame)
                self.normal_value_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

                ctk.CTkLabel(limits_frame, text="Dangerous Value").grid(row=1, column=0, padx=10, pady=5, sticky="e")
                self.dangerous_value_entry = ctk.CTkEntry(limits_frame)
                self.dangerous_value_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

                ctk.CTkLabel(limits_frame, text="Deadly Value").grid(row=2, column=0, padx=10, pady=5, sticky="e")
                self.deadly_value_entry = ctk.CTkEntry(limits_frame)
                self.deadly_value_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

            self.root.update_idletasks()  # Update all widgets to calculate size
            popup_height = popup.winfo_reqheight() + 20  # Add vertical padding
            popup.geometry(f"600x{popup_height}")

        ctk.CTkLabel(popup, text="Value Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        value_type_menu = ctk.CTkOptionMenu(popup, values=["int", "float", "str"], command=show_input_menu_type)
        value_type_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def submit():           
            # Check if colour status boundaries are included for all sensors of type int and float.
            if value_type_menu.get() != "str" and self.colour_status_boundaries == []:
                CTkMessagebox(title="Warning", message="Colour status boundaries must be included for all sensors of type int or float", icon="warning")
                return

            # Clear any colour status boundaries if str sensor is chosen
            if value_type_menu.get() == "str":
                self.colour_status_boundaries = []
                normal_limits = self.normal_value_entry.get()
                dangerous_limits = self.dangerous_value_entry.get()
                deadly_limits = self.deadly_value_entry.get()

            elif value_type_menu.get() == "int" or value_type_menu.get() == "float":
                print("normal limits min entry", self.normal_limits_min_entry.get())
                normal_limits={"min": int(self.normal_limits_min_entry.get()),"max": int(self.normal_limits_max_entry.get())}
                dangerous_limits={"min": int(self.dangerous_limits_min_entry.get()),"max": int(self.dangerous_limits_max_entry.get())}
                deadly_limits={"min": int(self.deadly_limits_min_entry.get()),"max": int(self.deadly_limits_max_entry.get())}

            self.manager.add_sensor(id=sensor_id_entry.get(),
                                    friendly_name=friendly_name_entry.get(),
                                    unit=unit_entry.get(),
                                    value_type=value_type_menu.get(),
                                    colour_status_boundaries= self.colour_status_boundaries,
                                    normal_limits=normal_limits,
                                    dangerous_limits=dangerous_limits,
                                    deadly_limits=deadly_limits)

            self.sensor_count += 1
            self.colour_status_boundaries.clear()

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
            # popup.destroy() # TODO: uncomment when finished testing

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

