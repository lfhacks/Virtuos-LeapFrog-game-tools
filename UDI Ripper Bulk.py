import struct
import zlib
from PIL import Image
from pathlib import Path

filelist = list(Path('.').glob('*.udi'))

def rgba5551_to_argb1555(rgba_data):
    argb_data = bytearray(len(rgba_data))  # Same length since it's still 16 bits per pixel
    for i in range(0, len(rgba_data), 2):
        # Extract the 16-bit pixel value
        pixel = (rgba_data[i] << 8) | rgba_data[i + 1]
        
        # Extract the RGBA components
        r = (pixel >> 11) & 0x1F  # Red: bits 15:11
        g = (pixel >> 6) & 0x1F  # Green: bits 10:6
        b = (pixel >> 1) & 0x1F  # Blue: bits 5:1
        a = pixel & 0x1        # Alpha: bit 0
        
        # Reassemble in ARGB1555 order
        argb_pixel = (a << 15) | (r << 10) | (g << 5) | b
        
        # Store the ARGB1555 pixel value
        argb_data[i] = argb_pixel >> 8
        argb_data[i + 1] = argb_pixel & 0xFF
    
    return argb_data

for files in filelist:
    with open(files, "rb") as file:
        magic, unknown1, unknown2, unknown3 = struct.unpack("<4I", file.read(16))
        if magic != 4801621: # UDI\x00
            raise ValueError("Magic check failed: not a UDI file!")
        width, height = struct.unpack("<2H", file.read(4))
        print(width, height)
        unknown4, unknown5 = struct.unpack("<2I", file.read(8))
        redbits, greenbits, bluebits, alphabits, = struct.unpack("<4B", file.read(4))
        channelmap = struct.unpack("<I", file.read(4))
        imagedata = zlib.decompress(file.read())
        print(redbits, greenbits, bluebits, alphabits)
        if redbits == 4 and greenbits == 4 and bluebits == 4 and alphabits == 4:
            rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA;4B")
            # quick hack to get around PIL's lack of little-endian RGBA4 support
            rawimage = Image.merge('RGBA', rawimage.split()[::-1])
            rawimage.save(files.with_suffix(".png"))
        if redbits == 8 and greenbits == 8 and bluebits == 8 and alphabits == 8:
            rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA")
            rawimage.save(files.with_suffix(".png"))
        if redbits == 5 and greenbits == 5 and bluebits == 5 and alphabits == 1:
            print("RGBA5551")
            imagedata_swapped = rgba5551_to_argb1555(imagedata)
            rawimage = Image.frombytes("RGBA", (width, height), imagedata_swapped, "raw", "BGRA;15") # note - expects big endian. UDIs tend to be little-endian.
            rawimage.save(files.with_suffix(".png"))
        if redbits == 5 and greenbits == 6 and bluebits == 5 and alphabits == 0:
            rawimage = Image.frombytes("RGB", (width, height), imagedata, "raw", "BGR;16")
            rawimage.save(files.with_suffix(".png"))
