
class Entity:
    def __init__(self, name, pos, vel, max_vel, sprite):
        self.name = name
        self.pos = pos  # Position
        self.vel = vel  # Velocity
        self.max_vel = max_vel  # Velocity cap
        self.sprite = sprite


class Player(Entity):
    def __init(self, name, pos, vel, max_vel, sprite):
        super().__init__(name, pos, vel, max_vel, sprite)
