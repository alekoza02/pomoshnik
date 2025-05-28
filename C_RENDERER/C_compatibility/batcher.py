import numpy as np
import ctypes
import os
import time
import pygame


class Batch:
    def __init__(self):
        self.dll = ctypes.CDLL(os.path.abspath("./C_RENDERER/C_bin/array_modifier.dll"))

        self.dll.modify_array.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),     #datadata
            ctypes.c_int,                       #width
            ctypes.c_int,                       #height
            ctypes.POINTER(ctypes.c_int),     #points_coords
            ctypes.c_int,                       #n_points
            ctypes.POINTER(ctypes.c_int),       #delimiters
            ctypes.c_int,                       #n_plots
            ctypes.POINTER(ctypes.c_uint8),     #colors
            ctypes.POINTER(ctypes.c_uint8)        #radii
        ]

    
    def update_canvas_size(self, w, h):
        self.w = int(w)
        self.h = int(h)

        self.canvas = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self.surface = pygame.Surface((self.w, self.h), depth=24)
        self.ptr_canvas = self.canvas.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        self.apply_array_to_surface()


    def render_batch(self, points, delimiters, colors, radii, bg=None):
        
        colors_rgba = np.append(colors, 127).astype(np.uint8)
        bg_rgba = np.append(bg, 255).astype(np.uint8)

        points = points.astype(np.int32)
        points = points[:, :2]
        if not points.flags['C_CONTIGUOUS']:
            points = np.ascontiguousarray(points)

        delimiters = np.array([delimiters], dtype=np.int32)
        colors = np.array([colors_rgba, bg_rgba], dtype=np.uint8)
        radii = np.array([radii], dtype=np.uint8)

        self.ptr_points = points.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.ptr_delimiters = delimiters.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.ptr_colors = colors.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        self.ptr_radii = radii.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

        start = time.perf_counter()
        self.dll.modify_array(self.ptr_canvas, self.w, self.h, self.ptr_points, len(points), self.ptr_delimiters, len(delimiters), self.ptr_colors, self.ptr_radii)  
        stop = time.perf_counter()
        return stop - start


    def apply_array_to_surface(self):
        pygame.pixelcopy.array_to_surface(self.surface, self.canvas.transpose(1, 0, 2))