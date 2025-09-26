import tkinter as tk
from tkinter import ttk, scrolledtext

# Modern color scheme
BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#007acc"
ENTRY_BG = "#3c3f41"
BUTTON_BG = "#007acc"
BUTTON_HOVER = "#005a9e"
TEXT_BG = "#3c3f41"

def on_enter_button(e):
    e.widget['background'] = BUTTON_HOVER

def on_leave_button(e):
    e.widget['background'] = BUTTON_BG

def calculate_frames():
    try:
        # Get time inputs and split by comma
        time_input = entry_time.get().strip()
        if not time_input:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Please enter at least one time value")
            return
        
        time_values = [t.strip() for t in time_input.split(",") if t.strip()]
        
        if not time_values:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Please enter valid time values")
            return
        
        # Get FPS from dropdown
        fps = int(fps_var.get())
        
        # Clear previous results
        result_text.delete(1.0, tk.END)
        
        # Calculate frames for each time value
        total_all_frames = 0
        results = []
        
        for i, time_val in enumerate(time_values):
            if "." not in time_val:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: Invalid format for '{time_val}'. Use seconds.frames")
                return
            
            seconds_str, frames_str = time_val.split(".")
            seconds = int(seconds_str)
            frames = int(frames_str)
            
            # Validate frames value
            if frames >= fps:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: Frames value ({frames}) cannot be ≥ FPS ({fps}) for '{time_val}'")
                return
            
            total_frames = seconds * fps + frames
            total_all_frames += total_frames
            
            # Add to results text
            result_text.insert(tk.END, f"• {time_val} = {total_frames} frames\n")
        
        # Add total if multiple values
        if len(time_values) > 1:
            result_text.insert(tk.END, f"\nTotal: {total_all_frames} frames")
        
    except ValueError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")

def clear_all():
    entry_time.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    entry_time.focus()

def paste_from_clipboard():
    try:
        clipboard = root.clipboard_get()
        entry_time.delete(0, tk.END)
        entry_time.insert(0, clipboard)
    except:
        pass

# GUI Setup
root = tk.Tk()
root.title("Frame Calculator Pro")
root.geometry("500x500")
root.configure(bg=BG_COLOR)

# Set modern theme
style = ttk.Style()
style.theme_use('clam')

# Configure styles
style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Segoe UI', 10))
style.configure('TButton', background=BUTTON_BG, foreground=FG_COLOR, font=('Segoe UI', 9))
style.configure('TCombobox', fieldbackground=ENTRY_BG, background=ENTRY_BG, foreground=FG_COLOR)

# Main frame
main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(main_frame, text="Frame Calculator", 
                      font=('Segoe UI', 16, 'bold'), 
                      bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(pady=(0, 20))

# Input frame
input_frame = tk.Frame(main_frame, bg=BG_COLOR)
input_frame.pack(fill=tk.X, pady=(0, 15))

# Time input
time_label = tk.Label(input_frame, text="Time Input (seconds.frames):", 
                     bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 10))
time_label.pack(anchor=tk.W)

entry_time = tk.Entry(input_frame, font=('Segoe UI', 10), 
                     bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                     relief='flat', width=40)
entry_time.pack(fill=tk.X, pady=(5, 5))

# Example label
example_label = tk.Label(input_frame, text="Examples: 1.14, 2.24, 3.05", 
                        bg=BG_COLOR, fg="#888888", font=('Segoe UI', 8))
example_label.pack(anchor=tk.W)

# FPS selection frame
fps_frame = tk.Frame(main_frame, bg=BG_COLOR)
fps_frame.pack(fill=tk.X, pady=(0, 20))

fps_label = tk.Label(fps_frame, text="Frame Rate:", 
                    bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 10))
fps_label.pack(side=tk.LEFT)

# FPS dropdown
fps_var = tk.StringVar(value="30")
fps_dropdown = ttk.Combobox(fps_frame, textvariable=fps_var, 
                           width=8, state="readonly", font=('Segoe UI', 10))
fps_dropdown['values'] = ("24", "25", "30", "60", "120", "240")
fps_dropdown.pack(side=tk.LEFT, padx=(10, 0))

# Buttons frame
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(fill=tk.X, pady=(0, 20))

calc_button = tk.Button(button_frame, text="Calculate Frames", 
                       command=calculate_frames, font=('Segoe UI', 10),
                       bg=BUTTON_BG, fg=FG_COLOR, relief='flat', padx=20)
calc_button.pack(side=tk.LEFT, padx=(0, 10))

clear_button = tk.Button(button_frame, text="Clear All", 
                        command=clear_all, font=('Segoe UI', 10),
                        bg="#555555", fg=FG_COLOR, relief='flat', padx=20)
clear_button.pack(side=tk.LEFT)

paste_button = tk.Button(button_frame, text="Paste", 
                        command=paste_from_clipboard, font=('Segoe UI', 10),
                        bg="#555555", fg=FG_COLOR, relief='flat', padx=20)
paste_button.pack(side=tk.RIGHT)

# Add hover effects
calc_button.bind("<Enter>", on_enter_button)
calc_button.bind("<Leave>", on_leave_button)
clear_button.bind("<Enter>", on_enter_button)
clear_button.bind("<Leave>", on_leave_button)
paste_button.bind("<Enter>", on_enter_button)
paste_button.bind("<Leave>", on_leave_button)

# Results area
results_label = tk.Label(main_frame, text="Results:", 
                        bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 11, 'bold'))
results_label.pack(anchor=tk.W, pady=(10, 5))

result_text = scrolledtext.ScrolledText(main_frame, height=12, 
                                       bg=TEXT_BG, fg=FG_COLOR,
                                       font=('Consolas', 10),
                                       relief='flat', padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

# Focus on input field when app starts
entry_time.focus()

# Run the application
root.mainloop()