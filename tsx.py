# tsx.py - wrapper for the Virtuos TextureSheet/tsx format

import sys
import xml.etree.ElementTree
from PIL import Image
import udi

e = xml.etree.ElementTree.parse(sys.argv[1])
r = e.getroot()

if r[0].attrib['Count'] != '1':
    print('note: texture sheets involving multiple pages aren\'t implemented right now. Exiting.')
    exit()
pages = []
for page in r[0]:
    pages.append(udi.filename_to_image(page.attrib['Path']))
for frame in r[1]:
    if frame.attrib['RegionCount'] != '1':
        continue
    region = frame[0]
    pageindex = int(region.attrib['PageIndex'])
    left = int(region.attrib['X'])
    upper = int(region.attrib['Y'])
    right = left + int(region.attrib['Width'])
    lower = upper + int(region.attrib['Height'])
    region_im = pages[pageindex].crop((left, upper, right, lower))
    region_im.save(frame.attrib['Name'] + '.png')

# print(sys.argv[1])
