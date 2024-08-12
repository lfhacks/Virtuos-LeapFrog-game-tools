import pygame
import numpy as np
import struct
import tkinter as tk #Used to kill the extra tkinter window
from tkinter import filedialog
root = tk.Tk()#Create a root window
root.withdraw()#Hide the root window
file = filedialog.askopenfilename()
root.destroy()#Destroy the root window

def triStrip(file_path, offset, tri_count, vCount):
    triangles = []
    with open(file_path, "rb") as f:
        f.seek(offset)
        strip = struct.unpack('<' + str(tri_count) + 'H', f.read(2 * tri_count))

    for i in range(tri_count - 2):
        v1, v2, v3 = strip[i], strip[i + 1], strip[i + 2]
        
        if i & 1:  #Odd faces
            triangles.append((v1, v2, v3))
        else:  #Even faces
            triangles.append((v2, v1, v3))
            

    return triangles

class SimpleRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Renderer for reverse engineering")
        self.clock = pygame.time.Clock()
        
        self.vertices = []
        self.faces = []
        
        #Camera properties
        self.camera_pos = np.array([0.0, 0.0, -5.0])
        self.camera_front = np.array([0.0, 0.0, 1.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.camera_right = np.cross(self.camera_front, self.camera_up)
        
        self.yaw = -90.0
        self.pitch = 0.0
        
        #Clipping range
        self.near_clip = -5
        self.far_clip = 100.0

    def load_obj(self, filename):
        
        DATA = b''
        
        with open(filename, 'rb') as file:
            for i in range(1): #Change this if you want to extract more models from the same file. Chances are, it will cause a crash, so be aware of that!
                with open(filename+f"{i}.obj", "w+") as o:
                    convertedVerts = []
                    convertedUVs = []
                    convertedFaces = []
                    self.vertices = []
                    self.faces = []
                    DATA = b''
                    DATA2 = b''
                    while DATA != b'DSPL':
                        if DATA != b'DSPL':
                            DATA = file.read(4)
                    DATA2 = file.read(1)
                    if DATA2 != b'\xFF':
                        file.seek(-1, 1)
                    else:
                        print(f"FF! {file.tell()}")
                        file.seek(7, 1)
                    while DATA != b'\xFF\xFF':
                        if DATA != b'\xFF\xFF':
                            DATA = file.read(2)
                    if DATA == b'\xFF\xFF':
                        while DATA != b'\x00':
                            if DATA != b'\x00':
                                DATA = file.read(1)
                    file.seek(0x13, 1)
                    triCount, vertCount = struct.unpack("<II", file.read(8))
                    print(triCount, vertCount)
                    self.faces = triStrip(filename, file.tell(), triCount, vertCount)
                    for face in self.faces:
                        f = f"f {face[0]+1}/{face[0]+1}/{face[0]+1} {face[1]+1}/{face[1]+1}/{face[1]+1} {face[2]+1}/{face[2]+1}/{face[2]+1}\n"
                        convertedFaces.append(f)
                    file.seek(triCount*2, 1)
                    for vert in range(vertCount):
                        X, Y, Z, UX, UY, UZ = struct.unpack("<iiiiii", file.read(0x18))
                        VERT = [X/40000, Y/40000, Z/40000]
                        v = f"v {X/65535} {Y/65535} {Z/65535}\n"
                        vt= f"vt {UX/65535} {(UY*-1/65535)+1}\n"
                        convertedVerts.append(v)
                        convertedUVs.append(vt)
                        self.vertices.append(VERT)
                    for vertex in convertedVerts:
                        o.write(vertex)
                    for vertex in convertedUVs:
                        o.write(vertex)
                    for face in convertedFaces:
                        o.write(face)
    def project(self, point):
        point = point - self.camera_pos
        
        view_matrix = np.array([
            self.camera_right,
            self.camera_up,
            self.camera_front
        ])
        
        point = np.dot(view_matrix, point)
        
        if point[2] < self.near_clip or point[2] > self.far_clip:
            return None
        
        factor = 200 / (point[2] + 5)
        x = point[0] * factor + self.width / 2
        y = -point[1] * factor + self.height / 2
        return int(x), int(y)
    
    def draw_wireframe(self):
        if len(self.faces) > 0:
            for face in self.faces:
                points = []
                for vertex_index in face:
                    projected_point = self.project(self.vertices[vertex_index])
                    if projected_point is not None:
                        points.append(projected_point)
                
                if len(points) >= 2:
                    for i in range(len(points)):
                        start = points[i]
                        end = points[(i+1) % len(points)]
                        pygame.draw.line(self.screen, (255, 255, 255), start, end)
        else:
            self.draw_vertices()
    
    def draw_vertices(self):
        for vertex in self.vertices:
            pos = self.project(vertex)
            if pos is not None:
                pygame.draw.circle(self.screen, (255, 0, 0), pos, 2)
    
    def update_camera(self):
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = front / np.linalg.norm(front)
        self.camera_right = np.cross(self.camera_front, np.array([0.0, 1.0, 0.0]))
        self.camera_right /= np.linalg.norm(self.camera_right)
        self.camera_up = np.cross(self.camera_right, self.camera_front)
    
    def run(self):
        running = True
        vertex_view = False
        mouse_sensitivity = 0.1
        movement_speed = 0.1
        
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        vertex_view = not vertex_view
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.rel
                    self.yaw += x * mouse_sensitivity
                    self.pitch -= y * mouse_sensitivity
                    self.pitch = max(-89.0, min(89.0, self.pitch))
                    self.update_camera()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.camera_pos += movement_speed * self.camera_front
            if keys[pygame.K_s]:
                self.camera_pos -= movement_speed * self.camera_front
            if keys[pygame.K_a]:
                self.camera_pos -= movement_speed * self.camera_right
            if keys[pygame.K_d]:
                self.camera_pos += movement_speed * self.camera_right
            if keys[pygame.K_SPACE]:
                self.camera_pos += movement_speed * self.camera_up
            if keys[pygame.K_LSHIFT]:
                self.camera_pos -= movement_speed * self.camera_up
            
            self.screen.fill((0, 0, 0))
            if vertex_view:
                self.draw_vertices()
            else:
                self.draw_wireframe()
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()

#Read the file and display it (and convert to wavefront.obj)
if __name__ == "__main__":
    renderer = SimpleRenderer(800, 600)
    renderer.load_obj(file)
    renderer.run()
