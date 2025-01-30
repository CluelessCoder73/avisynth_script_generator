import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_avisynth_scripts():
    # Select folder containing videos
    folder_path = filedialog.askdirectory(title="Select folder containing videos")
    if not folder_path:
        return

    # Get user preferences
    source_filter = source_var.get()
    resizer = resizer_var.get()
    
    # Process each video in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.mkv', '.avi')):  # Add more video extensions if needed
            video_path = os.path.join(folder_path, filename).replace('/', '\\')
            script_content = f'''v={source_filter}("{video_path}")
a=LWLibavAudioSource("{video_path}")
audioDub(v, a)
{resizer}(1280, 720)
Deen(mode="c2d", rad=1, thrY=2, thrUV=4)
'''
            
            # Create AviSynth script file
            script_path = os.path.splitext(video_path)[0] + '.avs'
            with open(script_path, 'w') as f:
                f.write(script_content)
    
    messagebox.showinfo("Success", "AviSynth scripts created successfully!")

# Create GUI
root = tk.Tk()
root.title("AviSynth Script Generator")

# Source filter options
source_var = tk.StringVar(value="LWLibavVideoSource")
source_label = tk.Label(root, text="Source Filter:")
source_label.pack()
source_options = ["LWLibavVideoSource", "FFVideoSource", "DirectShowSource"]
source_menu = tk.OptionMenu(root, source_var, *source_options)
source_menu.pack()

# Resizer options
resizer_var = tk.StringVar(value="LanczosResize")
resizer_label = tk.Label(root, text="Resizer:")
resizer_label.pack()
resizer_options = ["LanczosResize", "BicubicResize", "Spline36Resize"]
resizer_menu = tk.OptionMenu(root, resizer_var, *resizer_options)
resizer_menu.pack()

# Create button
create_button = tk.Button(root, text="Create AviSynth Scripts", command=create_avisynth_scripts)
create_button.pack()

root.mainloop()
