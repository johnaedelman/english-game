import pygame
from lib.physics import *
from lib.entities import *
import sys

print("she call me hemingway when i frederic on her henry")

screen_size = (1280, 720)

pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

real = pygame.image.load("assets/sprites/quartz.png")
quartz = Entity("quartz", [(screen_size[0] - real.get_size()[0]) / 2, (screen_size[1] - real.get_size()[1]) / 2], [0, 0], 5, real)

while True:  # Begin the main loop
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Checks keypress for basic movement
        quartz.vel[1] = -15  # Note that this gets applied to his movement before it gets checked. Probably fix that
    if keys[pygame.K_d]:
        quartz.vel[0] += 1
    if keys[pygame.K_a]:
        quartz.vel[0] -= 1

    quartz.pos[0] += quartz.vel[0]
    quartz.pos[1] += quartz.vel[1]

    if not quartz.pos[1] >= screen_size[1] - quartz.sprite.get_height():
        quartz.vel[1] += 0.5
    else:
        quartz.vel[1] = 0
        quartz.pos[1] = screen_size[1] - quartz.sprite.get_height()

    vel_check_decay(quartz)

    print(quartz.vel)
    screen.blit(quartz.sprite, quartz.pos)
    pygame.display.update()

    main_clock.tick(60)  # Locks the game to run at 60 FPS
