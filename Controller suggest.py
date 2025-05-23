import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Initialize GUI
root = tk.Tk()
root.title("LED Pixel Calculator with Controller Suggestions")
root.geometry("350x250")  # Compact initial size to avoid content cutoff

# Load controller data
try:
    controller_df = pd.read_excel("controllers.xlsx")
except Exception as e:
    messagebox.showerror("File Error", f"Unable to read controllers.xlsx file.\n{e}")
    controller_df = pd.DataFrame()

def calculate_total_pixels():
    try:
        width_ft = float(width_entry.get())
        height_ft = float(height_entry.get())
        pixel_pitch_mm = float(pixel_pitch_entry.get())

        pixel_pitch_ft = pixel_pitch_mm / 304.8
        pixels_per_foot = 1 / pixel_pitch_ft

        width_px = round(width_ft * pixels_per_foot)
        height_px = round(height_ft * pixels_per_foot)
        total_pixels = width_px * height_px

        result_text = (
            f"Screen Resolution: {width_px} x {height_px} pixels\n"
            f"Total Pixels: {total_pixels:,} pixels\n"
        )

        if not controller_df.empty:
            suitable_controllers = controller_df[
                (controller_df["Max Pixels"] >= total_pixels) &
                (controller_df["Max Width"] >= width_px) &
                (controller_df["Max Height"] >= height_px)
            ]

            if not suitable_controllers.empty:
                result_text += "\nCompatible Controllers:\n"
                for _, row in suitable_controllers.iterrows():
                    result_text += (
                        f"- {row['Make']} {row['Model']} "
                        f"(Max Pixels: {row['Max Pixels']}, "
                        f"Max W: {row['Max Width']}, Max H: {row['Max Height']})\n"
                    )
            else:
                result_text += "\n❌ No compatible controllers found."
        else:
            result_text += "\n⚠️ Controller data not loaded."

        result_label.config(text=result_text)
        root.update_idletasks()
        root.geometry("")  # Let window resize naturally to fit content

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Heading
tk.Label(root, text="Pixel Calculator", font=("Arial", 16, "bold")).grid(
    row=0, column=0, columnspan=2, pady=(10, 20)
)

# Input Fields
tk.Label(root, text="Screen Width (ft):").grid(row=1, column=0, sticky="e", padx=10, pady=5)
width_entry = tk.Entry(root)
width_entry.grid(row=1, column=1, pady=5)

tk.Label(root, text="Screen Height (ft):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, pady=5)

tk.Label(root, text="Pixel Pitch (mm):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
pixel_pitch_entry = tk.Entry(root)
pixel_pitch_entry.grid(row=3, column=1, pady=5)

# Button
tk.Button(root, text="Calculate", command=calculate_total_pixels).grid(
    row=4, column=0, columnspan=2, pady=10
)

# Result Label (dynamically expands)
result_label = tk.Label(root, text="", font=("Arial", 10), justify="left", anchor="w")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Run the GUI
root.mainloop()

