import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def calculate_frames():
    try:
        # Get time inputs and split by comma
        time_input = entry_time.get().strip()
        if not time_input:
            raise ValueError("Please enter at least one time value")
        
        time_values = [t.strip() for t in time_input.split(",") if t.strip()]
        
        if not time_values:
            raise ValueError("Please enter valid time values")
        
        # Get FPS from dropdown
        fps = int(fps_var.get())
        
        # Clear previous results
        result_text.delete(1.0, tk.END)
        
        # Calculate frames for each time value
        results = []
        for i, time_val in enumerate(time_values):
            if "." not in time_val:
                raise ValueError(f"Please enter time as seconds.frames (e.g., 2.14) for value: {time_val}")
            
            seconds_str, frames_str = time_val.split(".")
            seconds = int(seconds_str)
            frames = int(frames_str)
            
            # Validate frames value
            if frames >= fps:
                raise ValueError(f"Frames value ({frames}) cannot be equal to or greater than FPS ({fps}) for time: {time_val}")
            
            total_frames = seconds * fps + frames
            
            # Add to results
            results.append(f"Time {i+1}: {time_val} = {total_frames} frames")
            
            # Also show in result text area
            result_text.insert(tk.END, f"{time_val} = {total_frames} frames\n")
        
        # Show summary in messagebox
        messagebox.showinfo("Results", "\n".join(results))
        
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def clear_all():
    entry_time.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Frame Calculator")
root.geometry("400x400")

# Main frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Time input
tk.Label(main_frame, text="Time (seconds.frames, comma-separated):").pack(anchor=tk.W, pady=(0, 5))
entry_time = tk.Entry(main_frame, width=40)
entry_time.pack(fill=tk.X, pady=(0, 10))

# Example label
example_label = tk.Label(main_frame, text="Example: 1.14, 2.24, 3.05", fg="gray", font=("Arial", 8))
example_label.pack(anchor=tk.W, pady=(0, 10))

# FPS selection frame
fps_frame = tk.Frame(main_frame)
fps_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(fps_frame, text="FPS (Frame Rate):").pack(side=tk.LEFT)

# FPS dropdown
fps_var = tk.StringVar(value="30")
fps_dropdown = ttk.Combobox(fps_frame, textvariable=fps_var, width=10, state="readonly")
fps_dropdown['values'] = ("24", "25", "30", "60", "120")
fps_dropdown.pack(side=tk.LEFT, padx=(5, 0))

# Buttons frame
button_frame = tk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=10)

tk.Button(button_frame, text="Calculate", command=calculate_frames, width=10).pack(side=tk.LEFT, padx=(0, 5))
tk.Button(button_frame, text="Clear", command=clear_all, width=10).pack(side=tk.LEFT)

# Results area
tk.Label(main_frame, text="Results:").pack(anchor=tk.W, pady=(10, 5))
result_text = scrolledtext.ScrolledText(main_frame, height=10, width=50)
result_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()