import tkinter as tk
from tkinter import messagebox

def calculate_frames():
    try:
        seconds = int(entry_seconds.get())
        frames = int(entry_frames.get())
        fps = int(entry_fps.get())

        total_frames = seconds * fps + frames
        messagebox.showinfo("Result", f"Total Frames: {total_frames}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# GUI Setup
root = tk.Tk()
root.title("Frame Calculator")
root.geometry("300x200")

# Seconds
tk.Label(root, text="Seconds:").pack(pady=5)
entry_seconds = tk.Entry(root)
entry_seconds.pack()

# Frames
tk.Label(root, text="Extra Frames:").pack(pady=5)
entry_frames = tk.Entry(root)
entry_frames.pack()

# FPS
tk.Label(root, text="FPS (Frame Rate):").pack(pady=5)
entry_fps = tk.Entry(root)
entry_fps.pack()

# Button
tk.Button(root, text="Calculate", command=calculate_frames).pack(pady=15)

root.mainloop()
