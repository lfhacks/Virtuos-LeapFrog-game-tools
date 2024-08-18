# Virtuos-LeapFrog-game-tools
A set of tools for researching the games made by Virtuos for the Leapster Explorer, LeapPad Explorer and LeapTV

Feel free to make modifications to any of the tools seen here for your own projects so long as the said modifications aren't malicious.

# Supported games

- LeapFrog Kart Racing (Supercharged)
- SpongeBob SquarePants: the Clam Prix
- Transformers: Rescue Bots

# Troubleshooting 

Q: "Why doesn't (game name)'s model conversion script run?" or "(game name)'s model conversion script throws an error when ran. How do I fix it?"

A: Be sure that PyGame is installed (it's used for the mesh renderer). Also be sure that numpy is installed. 

To do this, run the following commands in either your terminal or command prompt:

pip install pygame

pip install numpy

Model conversions are stored in the same folder as the model you opened. The same thing applies to texture conversions.

# Model renderer controls
Think of it like Minecraft fly mode but you can fly in whatever direction the camera is pointed at.

- WASD moves the camera forward, backwards, left and right
- Shift moves the camera down
- Space moves the camera up
- The mouse rotates the camera
- Escape closes out of the renderer

# Model renderer screenshots
(Please note that the jankiness is only visible in the renderer! The converted obj files don't have random extra triangles and edges everywhere.)

![image](https://github.com/user-attachments/assets/6b056fe8-2612-485d-8768-72810775495b)
![image](https://github.com/user-attachments/assets/cbcd1b1d-bb06-4e09-b3d8-f303e1de7e06)
![image](https://github.com/user-attachments/assets/31eb9aa1-8402-41c6-906a-c182c217fa1b)
![image](https://github.com/user-attachments/assets/67dcda3e-bf61-4e1f-9608-f83d94116b92)
![image](https://github.com/user-attachments/assets/205479e0-3da7-44b2-86ab-fc208491a237)

# To-do
- Write a conversion script for the UDI format (thank you applecuckoo! You helped a ton with the header information and documentation you provided.)
- Figure out how to tell the different versions of UDI, CAR and ZON apart so the model and texture extractors don't have to be game-specific
- Fully reverse engineer the model format (currently, all the script does is jump to "DSPL" and parse the mesh data. The header needs to be documented.)
- Reverse engineer the track format so course models can be ripped
- Properly convert the PKM images (they're stored as ETC2 RGB data with a very simple 16 byte long header)
