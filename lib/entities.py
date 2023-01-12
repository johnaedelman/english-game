from lib.base import *


class Entity:
    def __init__(self, name, **kwargs):
        self.name = name
        self.sprite = pygame.image.load("assets/sprites/default_sprite.png")
        self.pos = [(screen_size[0] - self.sprite.get_size()[0]) / 2, 0]  # Position
        self.vel = [0, 0]  # Velocity
        self.max_vel = 5  # Velocity cap
        self.facing = "LEFT"
        self.animation = [self.sprite]
        self.animation_index = 0
        self.hitbox = None

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.sprite = self.animation[0]

        if self.hitbox is None:
            self.hitbox = pygame.Rect((self.pos, (self.sprite.get_width(), self.sprite.get_height())))

    def animate(self):  # Should be called every frame
        if self.animation_index > len(self.animation) - 1:
            self.animation_index = 0
        self.sprite = self.animation[self.animation_index]
        if self.facing == "RIGHT":
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.animation_index += 1


class Player(Entity):
    def __init(self, name):
        super().__init__(name)
