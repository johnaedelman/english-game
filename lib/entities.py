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
        self.animations = []
        self.animation_index = 0
        self.hitbox = None
        self.last_collision = 0  # Stores the time at which the entity last collided with another entity

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.sprite = self.animation[0]
        try:
            self.pos = kwargs["pos"]
        except KeyError:
            self.pos[0] = (screen_size[0] - self.sprite.get_size()[0]) / 2

        if self.hitbox is None:
            self.hitbox = pygame.Rect((self.pos, (self.sprite.get_width(), self.sprite.get_height())))

    def animate(self):  # Should be called every frame
        if self.animation_index > len(self.animation) - 1:
            self.animation_index = 0
        if type(self.animation[self.animation_index]) == list:
            self.animation = self.animation[self.animation_index]
            self.animation_index = 0
        self.sprite = self.animation[self.animation_index]
        if self.facing == "RIGHT":
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.animation_index += 1

    def side_collision(self, other_entity):
        sides_touching = False
        if self.hitbox.colliderect(other_entity.hitbox):
            if self.hitbox.right < other_entity.hitbox.left + 15:
                sides_touching = True
            elif self.hitbox.left > other_entity.hitbox.right - 15:
                sides_touching = True
        return sides_touching


class Player(Entity):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.health = 3
        self.last_jump = 0  # The time when the player last jumped


class Enemy(Entity):
    def __init__(self, name, **kwargs):
        self.movespeed = 4.5
        super().__init__(name, **kwargs)
        self.max_vel = self.movespeed

    def check_direction(self, floor):
        if self.facing == "LEFT":
            if self.hitbox.left - self.movespeed <= floor[1][0]:
                self.facing = "RIGHT"
                self.vel[0] = self.movespeed
            else:
                self.vel[0] = -self.movespeed
        elif self.facing == "RIGHT":
            if self.hitbox.right + self.movespeed >= floor[1][1]:
                self.facing = "LEFT"
                self.vel[0] = -self.movespeed
            else:
                self.vel[0] = self.movespeed
