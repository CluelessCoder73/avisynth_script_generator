import os
import tkinter as tk
from tkinter import filedialog, messagebox, IntVar

def create_avisynth_scripts():
    folder_path = filedialog.askdirectory(title="Select folder containing videos")
    if not folder_path:
        return

    source_filter = source_var.get()
    resizer = resizer_var.get()
    use_resizer = use_resizer_var.get()
    width = width_var.get()
    height = height_var.get()
    use_deen = use_deen_var.get()
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.mkv', '.avi')):
            video_path = os.path.join(folder_path, filename).replace('/', '\\')
            script_path = os.path.splitext(video_path)[0] + '.avs'
            
            if os.path.exists(script_path):
                if not messagebox.askyesno("File Exists", f"The file {script_path} already exists. Do you want to overwrite it?"):
                    continue

            if source_filter == "LWLibavVideoSource":
                script_content = f'''v={source_filter}("{video_path}")
a=LWLibavAudioSource("{video_path}")
audioDub(v, a)
'''
            elif source_filter == "DirectShowSource":
                script_content = f'''{source_filter}("{video_path}")
'''
            elif source_filter == "FFVideoSource":
                script_content = f'''a=FFAudioSource("{video_path}")
v={source_filter}("{video_path}")
audioDub(v, a)
'''
            elif source_filter == "AVISource":
                script_content = f'''{source_filter}("{video_path}")
'''
            
            if use_resizer:
                script_content += f'{resizer}({width}, {height})\n'
            
            if use_deen:
                script_content += 'Deen(mode="c2d", rad=1, thrY=2, thrUV=4)\n'
            
            with open(script_path, 'w') as f:
                f.write(script_content)
    
    messagebox.showinfo("Success", "AviSynth scripts created successfully!")

root = tk.Tk()
root.title("AviSynth Script Generator")

source_var = tk.StringVar(value="LWLibavVideoSource")
source_label = tk.Label(root, text="Source Filter:")
source_label.pack()
source_options = ["LWLibavVideoSource", "FFVideoSource", "DirectShowSource", "AVISource"]
source_menu = tk.OptionMenu(root, source_var, *source_options)
source_menu.pack()

resizer_var = tk.StringVar(value="LanczosResize")
resizer_label = tk.Label(root, text="Resizer:")
resizer_label.pack()
resizer_options = ["LanczosResize", "BicubicResize", "Spline36Resize"]
resizer_menu = tk.OptionMenu(root, resizer_var, *resizer_options)
resizer_menu.pack()

use_resizer_var = IntVar(value=1)
use_resizer_check = tk.Checkbutton(root, text="Use Resizer", variable=use_resizer_var)
use_resizer_check.pack()

width_var = tk.IntVar(value=1280)
width_label = tk.Label(root, text="Width:")
width_label.pack()
width_entry = tk.Entry(root, textvariable=width_var)
width_entry.pack()

height_var = tk.IntVar(value=720)
height_label = tk.Label(root, text="Height:")
height_label.pack()
height_entry = tk.Entry(root, textvariable=height_var)
height_entry.pack()

use_deen_var = IntVar(value=1)
use_deen_check = tk.Checkbutton(root, text="Use Deen Filter", variable=use_deen_var)
use_deen_check.pack()

create_button = tk.Button(root, text="Create AviSynth Scripts", command=create_avisynth_scripts)
create_button.pack()

root.mainloop()
