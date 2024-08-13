#pragma author applecuckoo
#pragma description LeapFrog .UDI (User Defined Image) files

import type.magic;

enum RGBAEnum : u8 {
    Red,
    Green,
    Blue,
    Alpha
};

struct UDIHeader {
    type::Magic<"UDI\x00"> id;
    padding[4];
    u16 imageOffset;
    padding[2];
    u32 fileSize;
    u16 width;
    u16 height;
    padding[8];
    u8 channelBits[4];
    RGBAEnum channelOrder[4];
};

UDIHeader header @ 0x00;