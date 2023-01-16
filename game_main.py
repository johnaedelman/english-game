import pygame.time

from lib.physics import *
from lib.entities import *
import sys
import copy

print("she call me hemingway when i frederic on her henry")


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

terrain = pygame.image.load("assets/sprites/terrain.png")
marker = pygame.image.load("assets/sprites/marker.png")
henry = pygame.image.load("assets/sprites/henry.png")
henry_jump = pygame.image.load("assets/sprites/henry_jump.png")
quartz = pygame.image.load("assets/sprites/quartz.png")
augh = pygame.mixer.Sound("assets/sounds/augh.mp3")
boom = pygame.mixer.Sound("assets/sounds/vine_boom.mp3")
augh.set_volume(0.1)
boom.set_volume(0.2)
animation_cycle = [henry, henry, henry, henry, henry]
jump_animation = [henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, animation_cycle]
player = Player("player", animation=animation_cycle)
enemy = Entity("arnold", pos=[1200, 30])

loaded_entities = [player, enemy]
print(player.hitbox.width)
last_time = 0  # The number of elapsed milliseconds the last time this value was checked. Used for cooldowns. May need to create multiple, one for each cooldown
last_hit = 0

while True:  # Begin the main loop
    screen.fill((0, 162, 232))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()  # Checks keypresses to determine velocity changes and such
    if keys[pygame.K_SPACE]:
        if pygame.time.get_ticks() - last_time >= 500 and player.pos[1] == screen_size[1] - get_floor(player.pos, player)[0] - player.sprite.get_height():  # Checks if the cooldown is up and if the player is touching the floor
            augh.play()
            player.animation = jump_animation
            player.vel[1] = -14
            last_time = pygame.time.get_ticks()
    if keys[pygame.K_d]:
        player.vel[0] += 1
        player.facing = "RIGHT"
    if keys[pygame.K_a]:
        player.vel[0] -= 1
        player.facing = "LEFT"
    if keys[pygame.K_LALT] and keys[pygame.K_BACKSPACE]:
        sys.exit()

    for i in range(15):  # Adds some markers every hundred pixels, just for scale
        screen.blit(marker, (i * 100, 0))

    for entity in loaded_entities:
        entity.animate()
        vel_check_decay(entity)

        prev_frame_pos = copy.deepcopy(entity.pos)
        entity.pos[0] += entity.vel[0]
        entity.pos[1] += entity.vel[1]
        entity.hitbox = pygame.Rect(entity.pos, (entity.hitbox.width, entity.hitbox.height))
        terrain_collision(entity, prev_frame_pos)  # Ensures proper terrain collision

        for e in loaded_entities:  # Make this into entity collision. When enemies bump into each other they should change direction, when players bump into enemy sides they lose health but when they bump into enemy tops they kill the enemy
            if entity != e:  # Prevents entity from colliding with itself

                if entity.hitbox.colliderect(e.hitbox):
                    if type(entity) == Player:
                        if entity.hitbox.bottom > e.hitbox.top + 15:  # If the player touches the side of the enemy
                            if pygame.time.get_ticks() - last_hit >= 1000:  # Gives the player 1 second of invincibility between hits
                                entity.health -= 1
                                print(entity.health)
                                last_hit = pygame.time.get_ticks()
                        else:  # If the player touches the top of the enemy
                            player.vel[1] = -14
                            boom.play()
                            player.animation = jump_animation
                            loaded_entities.remove(e)   # Kill enemy

    render_offset = -(player.pos[0] - ((screen_size[0] - player.sprite.get_size()[0]) / 2))

    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (render_offset, 0))

    for entity in loaded_entities:
        entity.sprite.set_colorkey((255, 255, 255))  # Keys out white background from all sprites, allowing transparency
        if type(entity) == Player:
            screen.blit(entity.sprite, (((screen_size[0] - player.sprite.get_size()[0]) / 2), entity.pos[1]))
        else:
            screen.blit(entity.sprite, (render_offset + entity.pos[0], entity.pos[1]))  # Renders all entities to the screen

    pygame.display.update()

    main_clock.tick(60)  # Locks the game to run at 60 FPS
