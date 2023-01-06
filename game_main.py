from lib.physics import *
from lib.entities import *
import sys
import copy

print("she call me hemingway when i frederic on her henry")


pygame.init()
pygame.display.set_caption("A Farewell To Arms: The Game")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.jpg"))
screen = pygame.display.set_mode(screen_size)
main_clock = pygame.time.Clock()

terrain = pygame.image.load("assets/sprites/terrain.png")
marker = pygame.image.load("assets/sprites/marker.png")
henry = pygame.image.load("assets/sprites/henry.png")
quartz = pygame.image.load("assets/sprites/quartz.png")
animation_cycle = [henry, henry, henry, henry, henry]
player = Entity("player", animation=animation_cycle)

floor = [
    [0, 540, 200],  # Lower bound on x-axis, upper bound on x-axis, y-value to set as floor
    [541, 1080, 400]
]


def get_floor(position):
    offset = 0
    return_interval = [0, 0, 0]
    for interval in floor:
        if (interval[1] >= position[0] >= interval[0]) or (interval[1] >= position[0] + player.sprite.get_width() >= interval[0]):  # The left and right edges of the sprite both have to be within the interval to avoid clipping
            offset = interval[2]  # Potential bug here - multiple intervals can be a match to the same x-pos. Has not caused problems yet, but be aware of it
            return_interval = interval
    return offset, return_interval


last_time = 0  # The number of elapsed milliseconds the last time this value was checked. Used for cooldowns. May need to create multiple, one for each cooldown

while True:  # Begin the main loop
    screen.fill((0, 162, 232))
    terrain.set_colorkey((255, 255, 255))
    screen.blit(terrain, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the game window has been closed. If so, stops the program
            sys.exit()

    keys = pygame.key.get_pressed()  # Checks keypresses to determine velocity changes and such
    if keys[pygame.K_SPACE]:
        if pygame.time.get_ticks() - last_time >= 500 and player.pos[1] == screen_size[1] - get_floor(player.pos)[0] - player.sprite.get_height():  # Checks if the cooldown is up and if the player is touching the floor
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

    player.animate()

    for i in range(15):  # Adds some markers every hundred pixels, just for scale
        screen.blit(marker, (i * 100, 0))

    vel_check_decay(player)

    prev_pos = copy.deepcopy(player.pos)
    player.pos[0] += player.vel[0]
    player.pos[1] += player.vel[1]

    floor_offset = get_floor(player.pos)[0]

    if get_floor(player.pos)[0] != get_floor(prev_pos)[0]:  # If the current frame's floor offset is different from the previous frame
        if player.pos[1] >= screen_size[1] - player.sprite.get_height() - floor_offset:  # If the player's y-position is below the current floor
            player.vel[0] = 0
            player.pos[0] = prev_pos[0]  # Set the player back to where they were on the previous frame, meaning that the player won't be able to move into the wall
            floor_offset = get_floor(player.pos)[0]  # Changes the floor offset according to the new player position

    if not player.pos[1] >= screen_size[1] - player.sprite.get_height() - floor_offset:  # If the player is above the floor
        player.vel[1] += 0.5
    else:
        player.vel[1] = 0
        player.pos[1] = (screen_size[1] - player.sprite.get_height()) - floor_offset

    print(f"{player.vel} - {player.pos}")
    print(prev_pos)
    print(screen_size[1] - floor_offset - player.sprite.get_height())

    player.sprite.set_colorkey((255, 255, 255))
    screen.blit(player.sprite, player.pos)
    pygame.display.update()

    main_clock.tick(60)  # Locks the game to run at 60 FPS
