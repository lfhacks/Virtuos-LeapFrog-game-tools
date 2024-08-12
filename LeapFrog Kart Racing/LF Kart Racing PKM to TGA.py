#This script converts the PKM images used in LeapFrog Kart Racing Supercharged to much more easily viewed TGA files
import struct
import math
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
file = filedialog.askopenfilename()
root.destroy()

def convert_image(input_file, output_file):
    with open(input_file, 'rb') as f:
        f.seek(0x10)
        image_data = f.read(os.path.getsize(file)-0x2D)
        print(hex(len(image_data)))
    rgb_values = []
    for i in range(0, len(image_data), 8):
        r, g, b, _ = struct.unpack('BBBB', image_data[i:i+4])
        rgb_values.append((b, g, r))
    num_pixels = len(rgb_values)
    image_size = int(math.sqrt(num_pixels))
    header = struct.pack('<BBBHHBHHHHBB', 
        0,      #ID length
        0,      #Color map type
        2,      #Image type
        0, 0,   #Color map specification
        0, 0, 0,#X and Y origin
        image_size, image_size,  #Width and height
        24,     #Bits per pixel
        0       #Image descriptor
    )
    with open(output_file, 'wb') as f:
        f.write(header)
        for y in range(image_size - 1, -1, -1):
            for x in range(image_size):
                pixel = rgb_values[y * image_size + x]
                f.write(struct.pack('<BBB', *pixel))
        f.write(b'\x00' * 8)
        f.write(b'TRUEVISION-XFILE.\x00')

input_file = file
output_file = f'{file}.tga'
convert_image(input_file, output_file)
