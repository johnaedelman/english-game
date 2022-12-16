
vel_constant = 0.125  # The amount which velocity decays by


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
