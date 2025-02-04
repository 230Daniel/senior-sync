from classes.sensor_sim_UI import SensorSimUI
import customtkinter as ctk



if __name__ == "__main__":
    root = ctk.CTk()
    app = SensorSimUI(root)
    root.mainloop()