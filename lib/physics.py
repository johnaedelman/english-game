

vel_constant = 0.125  # The amount which velocity decays by

def vel_check_decay(entity):  # Checks if the entity's velocity exceeds its maximum. If not, decays velocity so entity can come to a stop when moving

    if entity.vel[0] > vel_constant:
        entity.vel[0] -= vel_constant
    if entity.vel[0] < -vel_constant:
        entity.vel[0] += vel_constant
    if -vel_constant <= entity.vel[0] <= vel_constant:
        entity.vel[0] = 0

    for i in range(len(entity.vel)):  # Allows x and y vel to both be checked without explicitly stating entity.vel[0] and entity.vel[1]
        if entity.vel[i] < -entity.max_vel:
            entity.vel[i] = -entity.max_vel
    if entity.vel[0] > entity.max_vel:
        entity.vel[0] = entity.max_vel



