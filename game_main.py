from lib.physics import *
from lib.entities import *
from lib.gui import *
import sys
import copy

print("she call me hemingway when i frederic on her henry")


pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

terrain = pygame.image.load("assets/sprites/basebackground.jpg")
marker = pygame.image.load("assets/sprites/marker.png")
henry = pygame.image.load("assets/sprites/henry.png")
henry_jump = pygame.image.load("assets/sprites/henry_jump.png")
quartz = pygame.image.load("assets/sprites/quartz.png")
augh = pygame.mixer.Sound("assets/sounds/augh.mp3")
animation_cycle = [henry, henry, henry, henry, henry]
jump_animation = [henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, animation_cycle]
player = Entity("player", animation=animation_cycle)
enemy = Entity("arnold")


loaded_entities = [player, enemy]
print(player.hitbox.width)
last_time = 0  # The number of elapsed milliseconds the last time this value was checked. Used for cooldowns. May need to create multiple, one for each cooldown

while True:  # Begin the main loop
    screen.fill((255, 255, 255))
    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (0, 0))

player = Player("player", animation=henry_animations["DEFAULT"], animations=henry_animations)
enemy = Enemy("arnold", facing="RIGHT")
enemy2 = Enemy("enemy2", pos=[100, 0])
enemy3 = Enemy("jarulius", pos=[1080, 0])
powerup = Powerup("alcohol1", powerup_type="ALCOHOL", pos=[0, 0])
powerup2 = Powerup("alcohol2", powerup_type="ALCOHOL", pos=[100, 0])
powerup3 = Powerup("alcohol3", powerup_type="ALCOHOL", pos=[200, 0])

current_textbox = None
loaded_entities = [player, enemy, enemy2, enemy3, powerup, powerup2, powerup3]
frame_counter = 0

while True:  # Begin the main loop
    screen.fill((0, 162, 232))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()  # Checks keypresses to determine velocity changes and such
    if keys[pygame.K_SPACE]:
        if pygame.time.get_ticks() - player.last_jump >= 500 and player.pos[1] == screen_size[1] - get_floor(player.pos, player)[0] - player.hitbox.height:  # Checks if the cooldown is up and if the player is touching the floor
            jump.play()
            player.animation = player.animations["JUMP"]
            player.vel[1] = -14
            player.last_jump = pygame.time.get_ticks()
    if keys[pygame.K_d]:
        player.vel[0] += 1
        player.facing = "RIGHT"
    if keys[pygame.K_a]:
        player.vel[0] -= 1
        player.facing = "LEFT"
    if keys[pygame.K_LALT] and keys[pygame.K_BACKSPACE]:
        sys.exit()

    for entity in loaded_entities:
        if type(entity) == Enemy:
            entity.check_direction(get_floor(entity.pos, entity))  # Ensures the enemy is facing the correct direction and won't walk into a wall or fall off a cliff

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
                        if type(e) == Enemy:  # If the player is colliding with an enemy
                            if entity.hitbox.bottom > e.hitbox.top + 15:  # If the player touches anywhere except the top of the enemy
                                if pygame.time.get_ticks() - entity.last_collision >= 1000:  # Gives the player 1 second of invincibility between hits
                                    entity.health -= 1
                                    player.last_collision = pygame.time.get_ticks()
                                    riff.play()
                            else:  # If the player touches the top of the enemy
                                if pygame.time.get_ticks() - entity.last_collision >= 1000:
                                    player.vel[1] = -14
                                    boom.play()
                                    player.animation = player.animations["JUMP"]
                                    loaded_entities.remove(e)   # Kill enemy
                        elif type(e) == Powerup:
                            e.effect(entity)
                            drink.play()
                            loaded_entities.remove(e)
                            if player.check_jaundice():
                                current_textbox = Textbox(None, "You drank too much! You have contracted jaundice and will now move more slowly.", 2500, 50)

                    if type(entity) == Enemy and pygame.time.get_ticks() - entity.last_collision >= 1000 and type(e) != Powerup:  # Makes enemies turn around when colliding with other enemies or the player
                        if entity.facing == "LEFT":
                            entity.facing = "RIGHT"
                        elif entity.facing == "RIGHT":
                            entity.facing = "LEFT"
                        entity.last_collision = pygame.time.get_ticks()

    render_offset = -(player.pos[0] - ((screen_size[0] - player.sprite.get_size()[0]) / 2))  # Pos to offset everything by when rendering, allows camera movement

    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (render_offset, 0))

    for entity in loaded_entities:  # Renders entities to screen
        entity.sprite.set_colorkey((255, 255, 255))  # Keys out white background from all sprites, allowing transparency
        if type(entity) == Player:
            if pygame.time.get_ticks() - entity.last_collision >= 1000:
                screen.blit(entity.sprite, (((screen_size[0] - player.sprite.get_size()[0]) / 2), entity.pos[1]))
            else:
                if frame_counter % 5 == 0:  # Makes the player sprite blink to indicate invincibility frames
                    screen.blit(entity.sprite, (((screen_size[0] - player.sprite.get_size()[0]) / 2), entity.pos[1]))

        else:
            screen.blit(entity.sprite, (render_offset + entity.pos[0], entity.pos[1]))  # Renders all entities to the screen

    render_health(player.health, screen)  # You will never guess what this function does

    if current_textbox is not None:
        current_textbox.adjust_pos()
        screen.blit(current_textbox.sprite, current_textbox.pos)

    pygame.display.update()
    frame_counter += 1
    main_clock.tick(60)  # Locks the game to run at 60 FPS
