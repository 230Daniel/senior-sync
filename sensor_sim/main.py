from classes.sensor_sim_UI import SensorSimUI
import customtkinter as ctk



if __name__ == "__main__":
    try:
        root = ctk.CTk()
        app = SensorSimUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("goodbye")
        root.destroy()