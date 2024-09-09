# .UDI (User Defined Image)[^1] file structure

| Offset | Size | Description |
| ------ | ---- | ----------- |
| 0x00 | 4 | Magic number (UDI\x00) |
| 0x04 | 4 | Unknown |
| 0x08 | 2 | Image Offset (always 36) |
| 0x0a | 2 | Unknown |
| 0x0c | 4 | File Size |
| 0x10 | 2 | Width |
| 0x12 | 2 | Height |
| 0x14 | 8 | Unknown (compression if 1, no compression if 0?) |
| 0x1c | 4 | Channel Bit Rates (1 per channel, i.e. 0x05060500 for RGB565) |
| 0x20 | 4 | Channel Order (R = 0, G = 1, B = 2, A = 3) |

## Notes

The User Defined Image format is made up of 18x18 pixel tiles. The latter two rows and latter two columns of each tile bleed over to the surrounding tiles.

There is also some sort of mechanism that detects if certain tiles can be substituted for an existing tile to avoid saving duplicates.

The image data is compressed with zlib.

[^1]: This is according to debug symbols in the main executable for Transformers Rescue Bots: Race to the Rescue (trans.so). There is a class named 'UserDefineImage' under the 'UDImage' namespace, which is referred to by the 'LoadUDI' function.

Earlier versions of this format (specifically the one used in SpongeBob SquarePants: the Clam Prix) aren't tiled and are instead handled more like regular, non-tiled bitmaps
