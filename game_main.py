import pygame
import sys

print("she call me hemingway when i frederic on her henry")

screen_size = (1280, 720)

pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

real = pygame.image.load("assets/sprites/quartz.png")
real_pos = [(screen_size[0] - real.get_size()[0]) / 2, (screen_size[1] - real.get_size()[1]) / 2]

while True:  # Begin the main loop
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        real_pos[1] -= 1
    if keys[pygame.K_s]:
        real_pos[1] += 1
    if keys[pygame.K_d]:
        real_pos[0] += 1
    if keys[pygame.K_a]:
        real_pos[0] -= 1

    screen.blit(real, real_pos)
    pygame.display.update()

    main_clock.tick(60)  # Locks the game to run at 60 FPS

