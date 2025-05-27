// x86_64-w64-mingw32-gcc -O3 -march=native -mtune=native -ffast-math -fomit-frame-pointer -flto -shared -o C_bin/array_modifier.dll C_lib/array_modifier.c

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#define CLAMP(val, min, max) ((val) < (min) ? (min) : ((val) > (max) ? (max) : (val)))

// Precompute blending
static inline uint8_t blend(uint8_t fg, uint8_t bg, float alpha) {
    return (uint8_t)(alpha * fg + (1.0f - alpha) * bg);
}

DLL_EXPORT void modify_array(uint8_t *restrict data, int width, int height,
                             int *restrict points_coords, int n_points,
                             int *restrict delimiters, int n_plots,
                             uint8_t *restrict colors, uint8_t *restrict radii) {

    int size = width * height * 3;

    // Background fill
    {
        uint8_t bg_R = colors[n_plots * 4 + 0];
        uint8_t bg_G = colors[n_plots * 4 + 1];
        uint8_t bg_B = colors[n_plots * 4 + 2];

        for (int i = 0; i < size; i += 3) {
            data[i + 0] = bg_R;
            data[i + 1] = bg_G;
            data[i + 2] = bg_B;
        }
    }

    // Draw scatter points
    int plot_number = -1;
    int next_delim = delimiters[0];
    for (int i = 0; i < n_points; i++) {

        if (i == next_delim) {
            plot_number++;
            next_delim = (plot_number + 1 < n_plots) ? delimiters[plot_number + 1] : n_points;

            // Cache color and alpha
            uint8_t color_r = colors[plot_number * 4 + 0];
            uint8_t color_g = colors[plot_number * 4 + 1];
            uint8_t color_b = colors[plot_number * 4 + 2];
            float color_a = (float)(colors[plot_number * 4 + 3]) / 255.0f;
            int radius = radii[plot_number];
            int lim_min = -radius / 2 + 1;
            int lim_max = radius / 2 + 1;

            // Write all points in this segment
            for (; i < next_delim; i++) {
                int x = points_coords[i * 2 + 0];
                int y = points_coords[i * 2 + 1];

                int y0 = y + lim_min;
                int y1 = y + lim_max;
                int x0 = x + lim_min;
                int x1 = x + lim_max;

                // Bounds check
                if (x0 < 0 || y0 < 0 || x1 >= width || y1 >= height)
                    continue;

                for (int dy = lim_min; dy < lim_max; dy++) {
                    int py = y + dy;
                    int row_base = py * width;
                    for (int dx = lim_min; dx < lim_max; dx++) {
                        int px = x + dx;
                        int idx = (row_base + px) * 3;

                        data[idx + 0] = blend(color_r, data[idx + 0], color_a);
                        data[idx + 1] = blend(color_g, data[idx + 1], color_a);
                        data[idx + 2] = blend(color_b, data[idx + 2], color_a);
                    }
                }
            }

            i--; // Adjust since loop will increment
        }
    }

    // Draw connecting lines (Bresenham)
    plot_number = -1;
    next_delim = delimiters[0];
    for (int i = 0; i < n_points - 1; i++) {
        if (i == next_delim) {
            plot_number++;
            next_delim = (plot_number + 1 < n_plots) ? delimiters[plot_number + 1] : n_points;
        }

        if (i + 1 == next_delim) continue;

        uint8_t color_r = colors[plot_number * 4 + 0];
        uint8_t color_g = colors[plot_number * 4 + 1];
        uint8_t color_b = colors[plot_number * 4 + 2];
        float color_a = (float)(colors[plot_number * 4 + 3]) / 255.0f;

        int x0 = points_coords[i * 2 + 0];
        int y0 = points_coords[i * 2 + 1];
        int x1 = points_coords[(i + 1) * 2 + 0];
        int y1 = points_coords[(i + 1) * 2 + 1];

        int dx = x1 - x0;
        int dy = y1 - y0;
        int abs_dx = dx > 0 ? dx : -dx;
        int abs_dy = dy > 0 ? dy : -dy;

        if (abs_dx > abs_dy) {
            if (x0 > x1) {
                int t;
                t = x0; x0 = x1; x1 = t;
                t = y0; y0 = y1; y1 = t;
                dx = x1 - x0;
                dy = y1 - y0;
            }

            int dir = dy < 0 ? -1 : 1;
            dy *= dir;

            int y = y0;
            int p = 2 * dy - dx;

            for (int j = 0; j <= dx; j++) {
                int px = x0 + j;
                if (px >= 0 && px < width && y >= 0 && y < height) {
                    int idx = (y * width + px) * 3;
                    data[idx + 0] = blend(color_r, data[idx + 0], color_a);
                    data[idx + 1] = blend(color_g, data[idx + 1], color_a);
                    data[idx + 2] = blend(color_b, data[idx + 2], color_a);
                }

                if (p >= 0) {
                    y += dir;
                    p -= 2 * dx;
                }
                p += 2 * dy;
            }
        } else {
            if (y0 > y1) {
                int t;
                t = x0; x0 = x1; x1 = t;
                t = y0; y0 = y1; y1 = t;
                dx = x1 - x0;
                dy = y1 - y0;
            }

            int dir = dx < 0 ? -1 : 1;
            dx *= dir;

            int x = x0;
            int p = 2 * dx - dy;

            for (int j = 0; j <= dy; j++) {
                int py = y0 + j;
                if (x >= 0 && x < width && py >= 0 && py < height) {
                    int idx = (py * width + x) * 3;
                    data[idx + 0] = blend(color_r, data[idx + 0], color_a);
                    data[idx + 1] = blend(color_g, data[idx + 1], color_a);
                    data[idx + 2] = blend(color_b, data[idx + 2], color_a);
                }

                if (p >= 0) {
                    x += dir;
                    p -= 2 * dy;
                }
                p += 2 * dx;
            }
        }
    }
}
