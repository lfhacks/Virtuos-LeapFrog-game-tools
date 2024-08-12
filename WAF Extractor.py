import os
import struct
import tkinter as tk
from tkinter import filedialog
import zlib
root = tk.Tk()
root.withdraw()
files = filedialog.askopenfilenames()
root.destroy()

def getString(file, offset): #Gets any 0 terminated string at any given offset. Useful for stuff like title info.
    string = ""
    scan = b'99'
    with open(file, "rb") as fileThatContainsString:
        fileThatContainsString.seek(offset)
        while scan != b'\x00':
            scan = fileThatContainsString.read(1)
            if scan != b'\x00':
                string = string+scan.decode("UTF-8")
    return string

def parseGDA(file, names, entries, outDir): #Contains the file data
    with open(file, "rb") as gda:
        for i in range(len(names)):
            gda.seek(entries[i][1])
            data = gda.read(entries[i][0])
            name = names[i].split("\\")
            outName = name[-1]
            path = ""
            for chunk in name:
                if chunk != name[-1]:
                    path += chunk+"/"
            if os.path.exists(outDir+path) == False:
                os.makedirs(outDir+path)
            with open(outDir+path+outName, "w+b") as out:
                out.write(data)
def parseGDF(file): #Contains the filename list
    names = []
    with open(file, "rb") as gdf:
        nameCount = struct.unpack("<I", gdf.read(4))[0]
        startOffset = nameCount*4+4
        for offset in range(nameCount):
            nameOffset = struct.unpack("<I", gdf.read(4))[0]+startOffset
            name = getString(file, nameOffset)
            names.append(name)
            print(name)
    return names

def parseGDT(file): #Contains the file offsets and sizes
    entries = []
    totalSize = 0
    with open(file, "rb") as gdt: 
        nothing = gdt.read(4)
        entryCount = struct.unpack("<I", gdt.read(4))[0]
        for data in range(entryCount):
            startOffset = struct.unpack("<I", gdt.read(4))[0]
            size = struct.unpack("<I", gdt.read(4))[0]+29
            entries.append([size, startOffset])
    return entries
for file in files:
    base = os.path.basename(file).split(".")[0]
    outDir = os.getcwd()+f"/Output/{base}/"
    if os.path.exists(outDir) == False:
        os.makedirs(outDir)
    with open(file, "rb") as waf:
        magic, unknown, files = struct.unpack("<III", waf.read(12))
        gda = False
        for fileID in range(files):
            outPath = ""
            letters = struct.unpack("<I", waf.read(4))[0]
            name = waf.read(letters).decode("UTF-8")
            print(name)
            path = name.split("/")
            for folder in path:
                if folder != path[-1]:
                    outPath = outPath+"/"+folder+"/"
            if os.path.exists(outDir+outPath) == False:
                os.makedirs(outDir+outPath)
            unpackedSize, startOffset = struct.unpack("<II", waf.read(8))
            nextFile = waf.tell()
            waf.seek(startOffset)
            totalSize = 0
            fullData = b''
            while totalSize < unpackedSize:
                chunkSize = struct.unpack("<I", waf.read(4))[0]
                data = zlib.decompress(waf.read(chunkSize))
                totalSize += len(data)
                fullData += data
            with open(outDir+name, "w+b") as out:
                out.write(fullData)
            if "gda" in name:
                gda = True
            if "gdt" in name:
                entries = parseGDT(outDir+name)
            if "gdf" in name:
                names = parseGDF(outDir+name)
            waf.seek(nextFile)
        
if gda == True:
    parseGDA(outDir+"Data.gda", names, entries, outDir)
