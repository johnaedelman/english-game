from lib.base import *


class Entity:
    def __init__(self, name, **kwargs):
        self.name = name
        self.sprite = pygame.image.load("assets/sprites/default_sprite.png")
        self.pos = [(screen_size[0] - self.sprite.get_size()[0]) / 2, (screen_size[1] - self.sprite.get_size()[1]) / 2]  # Position
        self.vel = [0, 0]  # Velocity
        self.max_vel = 5  # Velocity cap
        self.facing = "LEFT"
        self.animation = [self.sprite]
        self.animation_index = 0

        for key, value in kwargs.items():
            setattr(self, key, value)

    def animate(self):
        if self.animation_index > len(self.animation) - 1:
            self.animation_index = 0
        self.sprite = self.animation[self.animation_index]
        if self.facing == "RIGHT":
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.animation_index += 1


class Player(Entity):
    def __init(self, name):
        super().__init__(name)
