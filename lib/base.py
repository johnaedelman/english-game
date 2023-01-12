import pygame

screen_size = (1280, 720)

terrain_floor = [
    [0, 540, 190],  # Lower bound on x-axis, upper bound on x-axis, y-value to set as floor
    [541, 1080, 390]
]

terrain_lines = [
    ((0, 520), (540, 520)),
    ((540, 320), (1080, 320)),
    ((540, 520), (540, 320))
]
