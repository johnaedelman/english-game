import pygame
from lib.physics import *
from lib.entities import *
import sys
import copy

print("she call me hemingway when i frederic on her henry")

screen_size = (1280, 720)

pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

terrain = pygame.image.load("assets/sprites/terrain.png")
marker = pygame.image.load("assets/sprites/marker.png")
real = pygame.image.load("assets/sprites/quartz.png")
quartz = Entity("quartz", [(screen_size[0] - real.get_size()[0]) / 2, (screen_size[1] - real.get_size()[1]) / 2], [0, 0], 5, real)

floor = [
    [0, 540, 200],  # Lower bound on x-axis, upper bound on x-axis, y-value to set as floor
    [541, 1080, 400]
]


def get_floor(position):
    offset = 0
    return_interval = [0, 0, 0]
    for interval in floor:
        if (interval[1] >= position[0] >= interval[0]) or (interval[1] >= position[0] + quartz.sprite.get_width() >= interval[0]):  # The left and right edges of the sprite both have to be within the interval to avoid clipping
            offset = interval[2]  # Potential bug here - multiple intervals can be a match to the same x-pos. Has not caused problems yet, but be aware of it
            return_interval = interval
    return offset, return_interval


while True:  # Begin the main loop
    screen.fill((0, 162, 232))
    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Checks keypress for basic movement
        quartz.vel[1] = -10
    if keys[pygame.K_d]:
        quartz.vel[0] += 1
    if keys[pygame.K_a]:
        quartz.vel[0] -= 1
    if keys[pygame.K_LALT] and keys[pygame.K_BACKSPACE]:
        sys.exit()

    for i in range(15):  # Adds some markers every hundred pixels, just for scale
        screen.blit(marker, (i * 100, 0))

    vel_check_decay(quartz)

    prev_pos = copy.deepcopy(quartz.pos)
    quartz.pos[0] += quartz.vel[0]
    quartz.pos[1] += quartz.vel[1]

    floor_offset = get_floor(quartz.pos)[0]

    if get_floor(quartz.pos)[0] != get_floor(prev_pos)[0]:  # If the current frame's floor offset is different from the previous frame
        if quartz.pos[1] >= screen_size[1] - quartz.sprite.get_height() - floor_offset:  # If the player's y-position is below the current floor
            quartz.vel[0] = 0
            quartz.pos[0] = prev_pos[0]  # Set the player back to where they were on the previous frame, meaning that the player won't be able to move into the wall
            floor_offset = get_floor(quartz.pos)[0]  # Changes the floor offset according to the new player position

    if not quartz.pos[1] >= screen_size[1] - quartz.sprite.get_height() - floor_offset:  # If the player is above the floor
        quartz.vel[1] += 0.5
    else:
        quartz.vel[1] = 0
        quartz.pos[1] = (screen_size[1] - quartz.sprite.get_height()) - floor_offset

    print(f"{quartz.vel} - {quartz.pos}")
    print(prev_pos)
    print(screen_size[1] - floor_offset - quartz.sprite.get_height())

    screen.blit(quartz.sprite, quartz.pos)
    pygame.display.update()

    main_clock.tick(60)  # Locks the game to run at 60 FPS
