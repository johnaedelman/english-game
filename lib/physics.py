from lib.base import *

vel_constant = 0.25  # The amount which velocity decays by


def vel_check_decay(entity):  # Checks if the entity's x-velocity exceeds its maximum. If not, decays velocity so entity can come to a stop when moving. y-vel handled separately
    if entity.vel[0] > vel_constant:
        entity.vel[0] -= vel_constant
    if entity.vel[0] < -vel_constant:
        entity.vel[0] += vel_constant
    if -vel_constant <= entity.vel[0] <= vel_constant:
        entity.vel[0] = 0

    if entity.vel[0] < -entity.max_vel:
        entity.vel[0] = -entity.max_vel
    if entity.vel[0] > entity.max_vel:
        entity.vel[0] = entity.max_vel
    if entity.vel[1] < -15:  # Ensures that the player will never clip through an enemy when falling from a great height
        entity.vel[1] = -15
    if entity.vel[1] > 15:
        entity.vel[1] = 15


def get_floor(position, entity):
    offset = 0
    return_interval = [0, 0, 0]
    for interval in terrain_floor:
        if (interval[1] >= position[0] >= interval[0]) or (interval[1] >= position[0] + entity.hitbox.width >= interval[0]):  # The left and right edges of the sprite both have to be within the interval to avoid clipping
            offset = interval[2]  # Potential bug here - multiple intervals can be a match to the same x-pos. Has not caused problems yet, but be aware of it
            return_interval = interval
    return offset, return_interval


def terrain_collision(entity, prev_pos):
    floor_offset = get_floor(entity.pos, entity)[0]

    if get_floor(entity.pos, entity)[0] != get_floor(prev_pos, entity)[0]:  # If the current frame's floor offset is different from the previous frame
        if entity.pos[1] >= screen_size[1] - entity.hitbox.height - floor_offset:  # If the entity's y-position is below the current floor
            entity.vel[0] = 0
            entity.pos[0] = prev_pos[0]  # Set the entity back to where they were on the previous frame, meaning that the entity won't be able to move into the wall
            floor_offset = get_floor(entity.pos, entity)[0]  # Changes the floor offset according to the new entity position

    if not entity.pos[1] >= screen_size[1] - entity.hitbox.height - floor_offset:  # If the entity is above the floor
        entity.vel[1] += 0.5
    else:
        entity.vel[1] = 0
        entity.pos[1] = (screen_size[1] - entity.hitbox.height) - floor_offset
