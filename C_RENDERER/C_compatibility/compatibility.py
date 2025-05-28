import pygame
import numpy as np
import ctypes
import os
import time

from batcher import Batch


# Window size
width, height = 1872, 1620
ctypes.windll.user32.SetProcessDPIAware()

# Initialize pygame
pygame.init()
font = pygame.font.SysFont("Courier New", 36)
screen = pygame.display.set_mode((width, height))

batch = Batch()

# PLOT GENERATION (15_000 points, resolution 1872x1620 pixels @ 700FPS)
#########################################################################################################
# Create points
n_plots = 3
points1 = np.loadtxt('./C_RENDERER/C_compatibility/benz.dat')
points2 = np.loadtxt('./C_RENDERER/C_compatibility/benznh2.dat')
points3 = np.loadtxt('./C_RENDERER/C_compatibility/benzno2.dat')

points = np.vstack([points1, points2, points3])
points = points[:, :2]
points[:, 0] -= np.min(points[:, 0])
points[:, 0] /= np.max(points[:, 0])
points[:, 0] *= (width * 0.95)
points[:, 0] += (width * 0.025)

points[:, 1] -= np.min(points[:, 1])
points[:, 1] /= np.max(points[:, 1])
points[:, 1] = 1 - points[:, 1]
points[:, 1] *= (height * 0.95)
points[:, 1] += (height * 0.025)

points = points.astype(np.int32)

n_points = len(points)

# Create colors
colors = np.zeros((n_plots + 1, 4), dtype=np.uint8)
colors[0] = [255, 100, 100, 20]
colors[1] = [100, 255, 100, 20]
colors[2] = [100, 100, 255, 20]
colors[3] = [40, 40, 40, 254]

# Create radii
radii = np.zeros(n_plots, dtype=np.uint8)
radii[0] = 4
radii[1] = 4
radii[2] = 4

# Create delimiters
delimiters = np.zeros(n_plots, dtype=np.int32)
delimiters[0] = 0
delimiters[1] = 5000
delimiters[2] = 10000
#########################################################################################################

batch.update_canvas_size(1872, 1620)

fps_hist = [0 for i in range(50)]
computation_time_hist = [0 for i in range(50)]

# Main loop
clock = pygame.time.Clock()
running = True
cycle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    computation_time = batch.render_batch(points, delimiters, colors, radii)
    computation_time_hist.pop(0); computation_time_hist.append(computation_time)
    
    batch.apply_array_to_surface()
    screen.blit(batch.surface, (0, 0))                                                                                          
    
    fps = clock.get_fps()
    fps_hist.pop(0); fps_hist.append(fps)

    if cycle % 50 == 0:
        text_surface = font.render(f"Total FPS: {sum(fps_hist) / len(fps_hist):.2f} | C process FPS: {1 / (sum(computation_time_hist) / len(computation_time_hist)):.2f} | Best previous FPS: {16}", True, (255, 0, 0))                                                   
    

    screen.blit(text_surface, (0, 0))                                                                                  


    clock.tick(0)
    pygame.display.flip()
    cycle += 1



pygame.quit()
