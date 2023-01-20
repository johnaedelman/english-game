from lib.physics import *
from lib.entities import *
from lib.gui import *
import sys
from copy import deepcopy

pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()
pygame.mixer.music.load("assets/sounds/italian_music.mp3")

player = Player("Henry", animation=henry_animations["DEFAULT"], animations=henry_animations)

enemy = Enemy("austrian1", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[1400, 340])
enemy2 = Enemy("austrian2", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[2200, 400])
enemy3 = Enemy("fastaustrian1", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[2800, 500], movespeed=7)
enemy4 = Enemy("austrian3", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[3300, 500])
enemy5 = Enemy("austrian4", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[3920, 350])
enemy6 = Enemy("austrian5", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[4300, 350])
enemy7 = Enemy("austrian6", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[4520, 350])
enemy8 = Enemy("fastaustrian2", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[5600, 450], movespeed=7)
enemy9 = Enemy("fastaustrian3", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[6780, 600], movespeed=7)
enemy10 = Enemy("fastaustrian4", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[7100, 600], movespeed=7)
enemy11 = Enemy("austrian7", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[9700, 600])
enemy12 = Enemy("fastaustrian5", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[10100, 600], movespeed=7)
enemy13 = Enemy("austrian8", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[10900, 400])
enemy14 = Enemy("austrian9", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[11780, 550])
enemy15 = Enemy("fastaustrian6", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[11980, 550], movespeed=7)
enemy16 = Enemy("fastaustrian7", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[12350, 550], movespeed=7)
enemy17 = Enemy("austrian10", animation=austrian_animations["DEFAULT"], animations=austrian_animations, pos=[12450, 550])

powerup = Powerup("alcohol1", powerup_type="ALCOHOL", pos=[1800, 0])
powerup2 = Powerup("alcohol2", powerup_type="ALCOHOL", pos=[3650, 0])
powerup3 = Powerup("alcohol3", powerup_type="ALCOHOL", pos=[5700, 0])
powerup4 = Powerup("alcohol4", powerup_type="ALCOHOL", pos=[9900, 0])
powerup5 = Powerup("alcohol5", powerup_type="ALCOHOL", pos=[11650, 0])
powerup6 = Powerup("coffeebeans", powerup_type="COFFEEBEANS", pos=[7900, 0])

friendly_entity_1 = FriendlyEntity("Rinaldi", pos=[7750, 0], animation=[rinaldi])
friendly_entity_2 = FriendlyEntity("Catherine", pos=[13400, 0], animation=catherine_animations["DEFAULT"], animations=catherine_animations)

textbox_1 = Textbox("Rinaldi: ", "Mama Mia! Frederic, baby! You look like death! It must be a terrible case of the jaundice. Here! Here, my good man! Have some delicious coffee beans, these are sure to get the alcohol out of your liver.", 6000, 30)
textbox_2 = Textbox("Henry: ", "Thanks, Rinaldi. I was beginning to fear for my life, with all these Austrians about. I hope all is well with Catherine.", 4000, 30)
textbox_3 = Textbox("Rinaldi: ", "Oh, I'm sure she's fine. No Austrian could capture old Miss Barkley. Good luck finding her, baby!", 4000, 30)
friendly_entity_1.conversation = [textbox_1, textbox_2, textbox_3]

textbox_4 = Textbox("Henry: ", "Oh, Catherine! I'm glad you're safe.", 4000, 50)
textbox_5 = Textbox("Catherine: ", "Henry! It's a joy to see you. I was never very worried about these Austrians, to be truthful. I was only wondering when you would come for me.", 5500, 30)
textbox_6 = Textbox("Henry: ", "Well, I'm here now, Cat. Shall we go get something to eat? I haven't had anything but grappa and coffee beans today. It's an injustice. I was born to eat.", 6000, 30)
friendly_entity_2.conversation = [textbox_4, textbox_5, textbox_6]

death_textbox = Textbox(None, "You died! Rinaldi and Catherine will have to bury your skeleton into the earth in a large hole, which they have dug with a shovel.", 5000, 40)
current_textbox = None
paused = False
ending_cutscene = False
loaded_entities = [player, enemy, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8, enemy9, enemy10, enemy11, enemy12, enemy13, enemy14, enemy15, enemy16, enemy17, powerup, powerup2, powerup3, powerup4, powerup5, powerup6, friendly_entity_1, friendly_entity_2]
frame_counter = 0

pygame.mixer.music.set_volume(0.23)
pygame.mixer.music.play(loops=-1)
while True:  # Begin the main loop
    screen.fill((0, 162, 232))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()  # Checks keypresses to determine velocity changes and such
    if not paused:
        if keys[pygame.K_d]:
            player.vel[0] += 1
            player.facing = "RIGHT"
            player.has_moved = True
            if player.pos[1] == screen_size[1] - get_floor(player.pos, player)[0] - player.hitbox.height:
                player.animation = player.animations["RUN"]
        elif keys[pygame.K_a]:
            player.vel[0] -= 1
            player.facing = "LEFT"
            player.has_moved = True
            if player.pos[1] == screen_size[1] - get_floor(player.pos, player)[0] - player.hitbox.height:
                player.animation = player.animations["RUN"]
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - player.last_jump >= 500 and player.pos[1] == screen_size[1] - get_floor(player.pos, player)[0] - player.hitbox.height:  # Checks if the cooldown is up and if the player is touching the floor
                jump.play()
                player.animation = player.animations["JUMP"]
                player.vel[1] = -14
                player.last_jump = pygame.time.get_ticks()
                player.has_moved = True
    if keys[pygame.K_LALT] and keys[pygame.K_BACKSPACE]:
        sys.exit()

    for entity in loaded_entities:
        if type(entity) == FriendlyEntity:
            if entity.check_on_screen(loaded_entities) and not entity.conversed:
                paused = True
                current_textbox = entity.run_conversation()
                if current_textbox is None:
                    paused = False
            if textbox_6.finished:  # If the final conversation with Catherine is over
                paused = True

        if not paused:
            if type(entity) == Enemy:
                entity.check_direction(get_floor(entity.pos, entity))  # Ensures the enemy is facing the correct direction and won't walk into a wall or fall off a cliff

            entity.animate()
            vel_check_decay(entity)

            prev_frame_pos = deepcopy(entity.pos)
            entity.pos[0] += entity.vel[0]
            entity.pos[1] += entity.vel[1]
            entity.hitbox = pygame.Rect(entity.pos, (entity.hitbox.width, entity.hitbox.height))
            terrain_collision(entity, prev_frame_pos)  # Ensures proper terrain collision

            for e in loaded_entities:  # Make this into entity collision. When enemies bump into each other they should change direction, when players bump into enemy sides they lose health but when they bump into enemy tops they kill the enemy
                if entity != e:  # Prevents entity from colliding with itself
                    if entity.hitbox.colliderect(e.hitbox):

                        if type(entity) == Player:
                            if type(e) == Enemy and entity.has_moved:  # If the player is colliding with an enemy
                                if entity.hitbox.bottom > e.hitbox.top + 15:  # If the player touches anywhere except the top of the enemy
                                    if pygame.time.get_ticks() - entity.last_collision >= 1000:  # Gives the player 1 second of invincibility between hits
                                        entity.health -= 1
                                        if entity.health <= 0:
                                            current_textbox = death_textbox
                                            paused = True
                                            loaded_entities.remove(entity)
                                        player.last_collision = pygame.time.get_ticks()
                                        hurt.play()
                                else:  # If the player touches the top of the enemy
                                    if pygame.time.get_ticks() - entity.last_collision >= 1000:
                                        player.vel[1] = -14
                                        crush.play()
                                        player.animation = player.animations["JUMP"]
                                        loaded_entities.remove(e)   # Kill enemy
                            elif type(e) == Powerup:
                                e.effect(entity)
                                loaded_entities.remove(e)
                                if player.check_jaundice():
                                    current_textbox = Textbox(None, "You drank too much! You have contracted jaundice and will now move more slowly.", 2500, 50)

                        if type(entity) == Enemy and type(e) != Powerup and type(e) != FriendlyEntity:  # Makes enemies turn around when colliding with other enemies or the player
                            if type(e) == Player:
                                if pygame.time.get_ticks() - entity.last_player_collision >= 1000:  # Tracks collision with player separately to reduce weird clipping
                                    if entity.facing == "LEFT":
                                        entity.facing = "RIGHT"
                                    elif entity.facing == "RIGHT":
                                        entity.facing = "LEFT"
                                    entity.last_player_collision = pygame.time.get_ticks()
                            elif pygame.time.get_ticks() - entity.last_collision >= 1000:
                                if entity.facing == "LEFT":
                                    entity.facing = "RIGHT"
                                elif entity.facing == "RIGHT":
                                    entity.facing = "LEFT"
                                entity.last_collision = pygame.time.get_ticks()

    render_offset = -(player.pos[0] - ((screen_size[0] - player.sprite.get_size()[0]) / 2))  # Pos to offset everything by when rendering, allows camera movement

    if textbox_6.finished:
        if not ending_cutscene:
            player.final_pos = deepcopy(player.pos)
            ending_cutscene = True
        render_offset = -(player.final_pos[0] - ((screen_size[0] - player.sprite.get_size()[0]) / 2))

    if ending_cutscene:
        player.pos[1] = (screen_size[1] - get_floor(player.pos, player)[0]) - player.hitbox.height
        player.pos[0] += 5
        friendly_entity_2.pos[0] += 5
        player.facing = "RIGHT"
        friendly_entity_2.facing = "RIGHT"
        player.animation = player.animations["RUN"]
        friendly_entity_2.animation = friendly_entity_2.animations["RUN"]
        player.animate()
        friendly_entity_2.animate()
        if player.pos[0] > player.final_pos[0] + 640:
            if current_textbox is None:
                current_textbox = Textbox("Jay Gatsby: ", f"Congratulations on the victory, old sport! Where am I, you ask? It's simple! Though you cannot see me, I am everywhere and everything. At any rate, your score for this round is as follows: {calculate_score(loaded_entities, player)}.", 14000, 28)
            if current_textbox.finished:
                sys.exit()

    screen.blit(background, (0, 0))

    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (render_offset - 720, 0))

    for entity in loaded_entities:  # Renders entities to screen
        entity.sprite.set_colorkey((255, 255, 255))  # Keys out white background from all sprites, allowing transparency
        if type(entity) == Player and not ending_cutscene:
            if not player.has_moved:
                if frame_counter % 5 == 0:  # Makes the player sprite blink to indicate invincibility frames
                    screen.blit(entity.sprite, (((screen_size[0] - player.sprite.get_size()[0]) / 2), entity.pos[1]))
            else:
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

    if current_textbox == death_textbox and current_textbox.finished:
        sys.exit()

    pygame.display.update()
    frame_counter += 1
    main_clock.tick(60)  # Locks the game to run at 60 FPS
