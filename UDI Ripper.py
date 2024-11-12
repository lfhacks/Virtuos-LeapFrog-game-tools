import struct
import zlib
from PIL import Image

filename = (input("What is the name of your file (leave out the .udi extension): "))

with open((filename + ".udi"), "rb") as file:
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
        rawimage.save((filename + ".png"))
        rawimage.show("UDI Parser")
    if redbits == 8 and greenbits == 8 and bluebits == 8 and alphabits == 8:
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA")
        rawimage.save((filename + ".png"))
        rawimage.show("UDI Parser")
    if redbits == 5 and greenbits == 5 and bluebits == 5 and alphabits == 1:
        raise ValueError("RGBA5551 file detected - please convert manually")
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "BGRA;15") # note - expects big endian. UDIs tend to be little-endian.
        rawimage.save((filename + ".png"))
        rawimage.show("UDI Parser")
    if redbits == 5 and greenbits == 6 and bluebits == 5 and alphabits == 0:
        rawimage = Image.frombytes("RGB", (width, height), imagedata, "raw", "BGR;16")
        rawimage.save((filename + ".png"))
        rawimage.show("UDI Parser")
