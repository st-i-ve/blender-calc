import tkinter as tk
from tkinter import ttk, scrolledtext, font as tkfont

# Orange & Black color scheme
BG_COLOR = "#121212"          # deep black
FG_COLOR = "#ffffff"          # white text
ACCENT_COLOR = "#ff7a00"      # primary orange
ACCENT_COLOR_ALT = "#ff8f33"  # lighter orange shade
ENTRY_BG = "#1f1f1f"          # dark entry background
BUTTON_BG = ACCENT_COLOR       # default button background
BUTTON_HOVER = "#cc6200"      # darker orange on hover
TEXT_BG = "#181818"           # dark text area

# Rounded Button (pill shaped) using Canvas
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None,
                 bg=BUTTON_BG, fg=FG_COLOR,
                 hover_bg=BUTTON_HOVER,
                 radius=18, padding=(16, 8),
                 font=("Segoe UI", 10, "bold")):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0)

        self.parent = parent
        self.text = text
        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.radius = radius
        self.padding_x, self.padding_y = padding
        self.tkfont = tkfont.Font(family=font[0], size=font[1], weight=(font[2] if len(font) > 2 else "normal"))

        text_width = self.tkfont.measure(self.text)
        text_height = self.tkfont.metrics('linespace')
        width = text_width + self.padding_x * 2 + 2
        height = text_height + self.padding_y * 2 + 2
        self.configure(width=width, height=height, cursor="hand2")

        # Draw the pill shape and text
        self._draw_shape(self.bg)
        self.create_text(width/2, height/2, text=self.text, fill=self.fg, font=self.tkfont, tags=("btn_text",))

        # Bind interactions
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw_shape(self, color):
        self.delete("shape")
        w = int(float(self["width"]))
        h = int(float(self["height"]))
        r = min(self.radius, h // 2)
        x1, y1, x2, y2 = 1, 1, w - 1, h - 1

        # Four corner arcs
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, style='pieslice', fill=color, outline=color, tags=("shape",))
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, style='pieslice', fill=color, outline=color, tags=("shape",))
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, style='pieslice', fill=color, outline=color, tags=("shape",))
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, style='pieslice', fill=color, outline=color, tags=("shape",))

        # Center and side rectangles to complete the pill
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline=color, tags=("shape",))
        self.create_rectangle(x1, y1 + r, x1 + r, y2 - r, fill=color, outline=color, tags=("shape",))
        self.create_rectangle(x2 - r, y1 + r, x2, y2 - r, fill=color, outline=color, tags=("shape",))

    def _on_enter(self, _):
        self.itemconfig("shape", fill=self.hover_bg, outline=self.hover_bg)

    def _on_leave(self, _):
        self.itemconfig("shape", fill=self.bg, outline=self.bg)

    def _on_press(self, _):
        # Slightly darken on press
        self.itemconfig("shape", fill=self.hover_bg, outline=self.hover_bg)

    def _on_release(self, _):
        self.itemconfig("shape", fill=self.bg, outline=self.bg)
        if self.command:
            try:
                self.command()
            except Exception:
                pass

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
        gpu_text.delete(1.0, tk.END)
        
        # Calculate frames for each time value and track max as total
        max_total_frames = 0
        
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
            if total_frames > max_total_frames:
                max_total_frames = total_frames
            
            # Add to results text
            result_text.insert(tk.END, f"• {time_val} = {total_frames} frames\n")
        
        # Show total as the HIGHEST input, not sum
        if len(time_values) >= 1:
            result_text.insert(tk.END, f"\nTotal (max from inputs): {max_total_frames} frames")
        
        # Update GPU distribution panel
        try:
            gpu_count = int(gpu_var.get())
        except Exception:
            gpu_count = 6
        
        if gpu_count <= 0:
            gpu_count = 6
        
        base = max_total_frames // gpu_count
        remainder = max_total_frames % gpu_count
        gpu_text.insert(tk.END, f"Total frames: {max_total_frames}\nGPUs: {gpu_count}\n\n")
        for idx in range(1, gpu_count + 1):
            assigned = base + (1 if idx <= remainder else 0)
            gpu_text.insert(tk.END, f"GPU {idx}: {assigned} frames\n")
        
    except ValueError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")

def clear_all():
    entry_time.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    gpu_text.delete(1.0, tk.END)
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
                      bg=BG_COLOR, fg=ACCENT_COLOR)
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
                        bg=BG_COLOR, fg="#ffb26b", font=('Segoe UI', 8))
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

calc_button = RoundedButton(button_frame, text="Calculate Frames",
                           command=calculate_frames, font=('Segoe UI', 10, 'bold'),
                           bg=BUTTON_BG, fg=FG_COLOR, hover_bg=BUTTON_HOVER,
                           radius=20, padding=(18, 10))
calc_button.pack(side=tk.LEFT, padx=(0, 10))

clear_button = RoundedButton(button_frame, text="Clear All",
                            command=clear_all, font=('Segoe UI', 10, 'bold'),
                            bg=ACCENT_COLOR_ALT, fg=FG_COLOR, hover_bg="#e07922",
                            radius=20, padding=(18, 10))
clear_button.pack(side=tk.LEFT, padx=(0, 10))

paste_button = RoundedButton(button_frame, text="Paste",
                            command=paste_from_clipboard, font=('Segoe UI', 10, 'bold'),
                            bg="#cc6200", fg=FG_COLOR, hover_bg="#b25800",
                            radius=20, padding=(18, 10))
paste_button.pack(side=tk.RIGHT)

# Results area
results_label = tk.Label(main_frame, text="Results:", 
                        bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 11, 'bold'))
results_label.pack(anchor=tk.W, pady=(10, 5))

result_text = scrolledtext.ScrolledText(main_frame, height=12, 
                                       bg=TEXT_BG, fg=FG_COLOR,
                                       font=('Consolas', 10),
                                       relief='flat', padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

# GPU Distribution Panel
gpu_panel = tk.Frame(main_frame, bg=BG_COLOR)
gpu_panel.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

gpu_title = tk.Label(gpu_panel, text="Render Distribution", 
                     bg=BG_COLOR, fg=ACCENT_COLOR, font=('Segoe UI', 12, 'bold'))
gpu_title.pack(anchor=tk.W, pady=(0, 5))

gpu_controls = tk.Frame(gpu_panel, bg=BG_COLOR)
gpu_controls.pack(fill=tk.X, pady=(0, 10))

gpu_label = tk.Label(gpu_controls, text="GPUs:", 
                     bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 10))
gpu_label.pack(side=tk.LEFT)

gpu_var = tk.StringVar(value="6")
gpu_dropdown = ttk.Combobox(gpu_controls, textvariable=gpu_var,
                            width=8, state="readonly", font=('Segoe UI', 10))
gpu_dropdown['values'] = ("6", "7", "8", "9")
gpu_dropdown.pack(side=tk.LEFT, padx=(10, 0))

gpu_text = scrolledtext.ScrolledText(gpu_panel, height=8,
                                     bg=TEXT_BG, fg=FG_COLOR,
                                     font=('Consolas', 10),
                                     relief='flat', padx=10, pady=10)
gpu_text.pack(fill=tk.BOTH, expand=True)

# Focus on input field when app starts
entry_time.focus()

# Run the application
root.mainloop()