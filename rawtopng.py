import os
import struct
import time
import threading
from tkinter import Tk, Label, Button, filedialog
from PIL import Image

def decode_argb1555(data):
    pixels = []
    for i in range(0, len(data), 2):
        word = struct.unpack_from('<H', data, i)[0]
        a = (word & 0x8000) >> 15
        r = (word & 0x7C00) >> 10
        g = (word & 0x03E0) >> 5
        b = word & 0x001F
        r = (r << 3) | (r >> 2)
        g = (g << 3) | (g >> 2)
        b = (b << 3) | (b >> 2)
        a = 255 if a else 0
        pixels.append((r, g, b, a))
    return pixels

def convert_raw_to_png(input_dir, output_dir, log_file):
    with open(log_file, "w") as log:
        files = [f for f in os.listdir(input_dir) if f.endswith(".raw")]
        total_files = len(files)
        for index, filename in enumerate(files):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "rb") as f:
                    f.read(128)  # Skip the 128-byte header
                    raw_data = f.read()
                    pixels = decode_argb1555(raw_data)
                    if len(pixels) != 512 * 448:
                        raise ValueError("Incorrect number of pixels")
                    img = Image.new('RGBA', (512, 448))
                    img.putdata(pixels)
                    img.save(os.path.join(output_dir, filename.replace(".raw", ".png")))
            except Exception as e:
                file_size = os.path.getsize(file_path)
                log.write(f"Error processing {filename}: {e}, File size: {file_size} bytes\n")
            progress_label.config(text=f"Processed {index + 1} of {total_files} files")
            root.update_idletasks()
            time.sleep(0.1)
        status_label.config(text="Conversion completed! Check log for errors.")

def select_input_dir():
    input_dir = filedialog.askdirectory()
    input_label.config(text=input_dir)
    return input_dir

def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_label.config(text=output_dir)
    return output_dir

def start_conversion():
    input_dir = input_label.cget("text")
    output_dir = output_label.cget("text")
    log_file = "conversion_errors.log"
    if input_dir and output_dir:
        threading.Thread(target=convert_raw_to_png, args=(input_dir, output_dir, log_file)).start()

root = Tk()
root.title("RAW to PNG Converter")

input_label = Label(root, text="Select input directory")
input_label.pack()
input_button = Button(root, text="Browse", command=select_input_dir)
input_button.pack()

output_label = Label(root, text="Select output directory")
output_label.pack()
output_button = Button(root, text="Browse", command=select_output_dir)
output_button.pack()

start_button = Button(root, text="Start Conversion", command=start_conversion)
start_button.pack()

progress_label = Label(root, text="Progress: 0 files processed")
progress_label.pack()

status_label = Label(root, text="")
status_label.pack()

root.mainloop()
