import tkinter as tk
from tkinter import messagebox

def calculate_frames():
    try:
        # Split seconds.frames input
        time_input = entry_time.get().strip()
        if "." not in time_input:
            raise ValueError("Please enter time as seconds.frames (e.g., 2.14)")

        seconds_str, frames_str = time_input.split(".")
        seconds = int(seconds_str)
        frames = int(frames_str)
        fps = int(entry_fps.get())

        total_frames = seconds * fps + frames
        messagebox.showinfo("Result", f"Total Frames: {total_frames}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers (e.g., 2.14 for time).")

# GUI Setup
root = tk.Tk()
root.title("Frame Calculator")
root.geometry("300x180")

# Time input
tk.Label(root, text="Time (seconds.frames):").pack(pady=5)
entry_time = tk.Entry(root)
entry_time.pack()

# FPS
tk.Label(root, text="FPS (Frame Rate):").pack(pady=5)
entry_fps = tk.Entry(root)
entry_fps.pack()

# Button
tk.Button(root, text="Calculate", command=calculate_frames).pack(pady=15)

root.mainloop()
