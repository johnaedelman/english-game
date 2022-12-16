
def vel_check_decay(entity):  # Checks if the entity's velocity exceeds its maximum. If not, decays velocity so entity can come to a stop when moving
    for i in range(len(entity.vel)):  # Allows x and y vel to both be checked without explicitly stating entity.vel[0] and entity.vel[1]
        if entity.vel[i] > entity.max_vel:
            entity.vel[i] = entity.max_vel
            continue  # Breaks from this iteration of the loop and continues to the next, meaning maximum velocities won't be decayed
        if entity.vel[i] < -entity.max_vel:
            entity.vel[i] = -entity.max_vel
            continue

        if entity.vel[i] > 0.075:
            entity.vel[i] -= 0.075
        if entity.vel[i] < -0.075:
            entity.vel[i] += 0.075
        if -0.075 < entity.vel[i] < 0.075:
            entity.vel[i] = 0
