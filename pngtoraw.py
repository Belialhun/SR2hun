import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk

def convert_png_to_1555argb(raw_path, png_path, header_path):
    # Nyissuk meg a PNG képet
    img = Image.open(png_path).convert('RGBA')
    pixels = img.load()
    
    # Kép szélessége és magassága
    width, height = img.size

    # Nyissuk meg a célfájlt írásra bináris módban
    with open(raw_path, 'wb') as raw_file:
        # Fejléc beolvasása és írása (csak az első 128 byte)
        with open(header_path, 'rb') as header_file:
            raw_file.write(header_file.read(128))
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                # Az alfa bitet állítsuk 1-re
                alpha = 1 << 15

                # Redukáljuk a színcsatornákat 5 bitre
                r = (r >> 3) & 0x1F
                g = (g >> 3) & 0x1F
                b = (b >> 3) & 0x1F

                # Bit eltolás és kombináció
                argb1555 = alpha | (r << 10) | (g << 5) | b

                # Írjuk ki a fájlba kis endián sorrendben
                raw_file.write(argb1555.to_bytes(2, byteorder='little'))

def select_png():
    global png_path
    png_path = filedialog.askopenfilename(title="Select PNG File", filetypes=[("PNG Files", "*.PNG"), ("png Files", "*.png")])
    png_label.config(text=png_path)

def select_raw_header():
    global raw_header_path
    raw_header_path = filedialog.askopenfilename(title="Select RAW Header File", filetypes=[("RAW Files", "*.raw")])
    raw_header_label.config(text=raw_header_path)

def select_input_directory():
    global input_directory
    input_directory = filedialog.askdirectory(title="Select Input Directory")
    input_dir_label.config(text=input_directory)

def generate_raw_files():
    if not input_directory:
        result_label.config(text="Please select an input directory.")
        return
    
    output_directory = os.path.join(os.getcwd(), "output")
    os.makedirs(output_directory, exist_ok=True)
    
    png_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.png')]
    
    if not png_files:
        result_label.config(text="No PNG files found in the selected directory.")
        return
    
    progress_bar['maximum'] = len(png_files)
    
    for i, png_file in enumerate(png_files):
        png_path = os.path.join(input_directory, png_file)
        raw_path = os.path.join(output_directory, os.path.splitext(png_file)[0] + ".raw")
        convert_png_to_1555argb(raw_path, png_path, raw_header_path)
        
        # Csak az első 458880 byte mentése
        with open(raw_path, 'rb') as raw_file:
            data = raw_file.read(458880)
        with open(raw_path, 'wb') as raw_file:
            raw_file.write(data)
        
        progress_bar['value'] = i + 1
        progress_percentage.set(f"{int((i + 1) / len(png_files) * 100)}%")
        root.update_idletasks()
    
    result_label.config(text="RAW files generated successfully!")

def generate_raw_file():
    raw_path = filedialog.asksaveasfilename(title="Save RAW File", defaultextension=".raw", filetypes=[("RAW Files", "*.raw")])
    convert_png_to_1555argb(raw_path, png_path, raw_header_path)
    
    # Csak az első 458880 byte mentése
    with open(raw_path, 'rb') as raw_file:
        data = raw_file.read(458880)
    with open(raw_path, 'wb') as raw_file:
        raw_file.write(data)
    
    result_label.config(text="RAW file generated successfully!")

def update_ui():
    if selection.get() == 1:
        select_png_button.grid(row=2, column=0, padx=10, pady=10)
        png_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        select_input_dir_button.grid_remove()
        input_dir_label.grid_remove()
        generate_button.config(text="Generate RAW File from Single PNG", command=generate_raw_file)
    else:
        select_png_button.grid_remove()
        png_label.grid_remove()
        select_input_dir_button.grid(row=2, column=0, padx=10, pady=10)
        input_dir_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        generate_button.config(text="Generate RAW Files from Directory", command=generate_raw_files)

root = tk.Tk()
root.title("")
root.configure(bg='#1E3D59')
root.geometry("950x800")

# Load custom font
font_path = "kain2.ttf"
font_size = 18

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", background="#5A2E0C", foreground="#D3D3D3", font=(font_path, font_size), bordercolor="#3E1F0A")
style.configure("TLabel", background="#1E3D59", foreground="#D3D3D3", font=(font_path, font_size))
style.configure("TEntry", background="#5A2E0C", foreground="#D3D3D3", font=(font_path, font_size), bordercolor="#3E1F0A")
style.configure("TProgressbar", background="#5A2E0C", foreground="#D3D3D3")

# Add image to the GUI
img = Image.open("sr2.jpg")
img = img.resize((920, 430), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)
img_label = tk.Label(root, image=photo, bg='#1E3D59', bd=0)
img_label.grid(row=0, column=0, columnspan=2, pady=10)

# Selection switch
selection_frame = tk.Frame(root, bg='#1E3D59')
selection_frame.grid(row=1, column=0, columnspan=2)

selection = tk.IntVar()
selection.set(1)
ttk.Radiobutton(selection_frame, text="Single PNG File", variable=selection, value=1, command=update_ui).pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(selection_frame, text="Directory of PNG Files", variable=selection, value=2, command=update_ui).pack(side=tk.LEFT, padx=5)

# File and directory selection buttons and labels
select_png_button = ttk.Button(root, text="Select PNG File", command=select_png)
png_label = ttk.Label(root, text="", anchor='center')

select_input_dir_button = ttk.Button(root, text="Select Input Directory", command=select_input_directory)
input_dir_label = ttk.Label(root, text="", anchor='center')

# Header file selection
ttk.Button(root, text="Select RAW Header File", command=select_raw_header).grid(row=4, column=0, padx=10, pady=10)
raw_header_label = ttk.Label(root, text="", anchor='center')
raw_header_label.grid(row=5, column=0, columnspan=2)

# Generate button
generate_button = ttk.Button(root)
generate_button.grid(row=6, column=0, columnspan=2)

# Progress bar and result label
progress_percentage = tk.StringVar()
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=700, style="TProgressbar")
progress_bar.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
progress_label = ttk.Label(root, textvariable=progress_percentage, background="#1E3D59", foreground="#D3D3D3", font=(font_path, font_size))
progress_label.grid(row=8, column=0, columnspan=2)

result_label = ttk.Label(root, text="")
result_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

update_ui()
root.mainloop()
