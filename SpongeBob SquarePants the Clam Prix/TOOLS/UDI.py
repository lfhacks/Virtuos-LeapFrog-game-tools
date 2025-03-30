from codingTools import * #Where most of the stuff I use is contained

def parseHeader(udi):
    magic = udi.read(4)
    if magic == b'UDI\x00':
        udi.read(8) #Unknown
        size = littleunpack.uint(udi.read(4))
        width = littleunpack.ushort(udi.read(2))
        height= littleunpack.ushort(udi.read(2))
        compCheck = littleunpack.uint(udi.read(4))
        udiType = udi.read(4)[0]
        bitsPerChannel = udi.read(4)
        channelOrder = udi.read(4)
        return udiType, size, width, height, compCheck, bitsPerChannel, channelOrder
    else:
        print("NOT A VALID VIRTUOS UDI FILE!\nThe script will close in 4 seconds.")
        time.sleep(4) #Give user enough time to see this
        quit()
def reverseChannelOrder(channelOrder):
    newChannelOrder = []
    for value in range(len(channelOrder)):
        newChannelOrder.append(channelOrder[3-value])
    channelOrder = newChannelOrder
    print(channelOrder)
    return channelOrder

file = dialogs.file()
decompressedData = False
decompressedBuffer = "decompressed.bin"
newChannelOrder = []
with open(file, "rb") as udi:
    udiType, size, width, height, compCheck, bitsPerChannel, channelOrder = parseHeader(udi)
    channelOrder = reverseChannelOrder(channelOrder)
    if compCheck == 1:
        decompressedData = fileTools.decompress(udi.read())
        with open(decompressedBuffer, "w+b") as buf:
            buf.write(decompressedData)
    if udiType == 3:
        if decompressedData == False:
            channelOrder = reverseChannelOrder(channelOrder)
            paletteData = imageData.customWidthsAndOrder(file, 0x24, 0, 256, 1, bitsPerChannel, channelOrder)
            pixels = []
            udi.seek(0x200, 1)
            for y in range(height):
                for x in range(width):
                    try:
                        pixel = paletteData[udi.read(1)[0]]
                    except:
                        pixel = (0, 0, 0)
                    pixels.append(pixel)
            TGATEST = imageData.generateTGA(width, height, pixels)
            with open("TestTGA.tga", "w+b") as tga:
                tga.write(TGATEST)
        else:
            channelOrder = reverseChannelOrder(channelOrder)
            paletteData = imageData.customWidthsAndOrder(decompressedBuffer, 0x24, 0, 256, 1, bitsPerChannel, channelOrder)
            pixels = []
            with open(decompressedBuffer, "rb") as buf:
                buf.seek(0x200)
                for y in range(height):
                    for x in range(width):
                        pixel = paletteData[buf.read(1)[0]]
                        pixels.append(pixel)
            TGATEST = imageData.generateTGA(width, height, pixels)
            with open("TestTGA.tga", "w+b") as tga:
                tga.write(TGATEST)
    if udiType == 4:
        if decompressedData == False:
            paletteData = imageData.customWidthsAndOrder(file, 0x24, 1, width, height, bitsPerChannel, channelOrder)
            TGATEST = imageData.generateTGA(width, height, paletteData)
            with open("TestTGA.tga", "w+b") as tga:
                tga.write(TGATEST)
        else:
            paletteData = imageData.customWidthsAndOrder(decompressedBuffer, 0, 1, width, height, bitsPerChannel, channelOrder)
            TGATEST = imageData.generateTGA(width, height, paletteData)
            with open("TestTGA.tga", "w+b") as tga:
                tga.write(TGATEST)
