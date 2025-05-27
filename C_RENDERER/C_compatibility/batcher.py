import numpy as np
import ctypes
import os
import time
import pygame


class Batch:
    def __init__(self, w, h):
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

        self.update_canvas_size(w, h)

    
    def update_canvas_size(self, w, h):
        self.w = w
        self.h = h

        self.canvas = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self.ptr_canvas = self.canvas.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))


    def render_batch(self, points, delimiters, colors, radii):
        
        self.ptr_points = points.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.ptr_delimiters = delimiters.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.ptr_colors = colors.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        self.ptr_radii = radii.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

        start = time.perf_counter()
        self.dll.modify_array(self.ptr_canvas, self.w, self.h, self.ptr_points, len(points), self.ptr_delimiters, len(delimiters), self.ptr_colors, self.ptr_radii)  
        stop = time.perf_counter()
        return stop - start


    def _get_buffer(self):
        return self.canvas.tobytes()
    

    def get_pygame_surface(self):
        return pygame.image.frombuffer(self._get_buffer(), (self.w, self.h), 'RGB')