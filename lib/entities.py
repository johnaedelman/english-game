from lib.base import *


class Entity:
    def __init__(self, name, **kwargs):
        self.name = name
        self.sprite = default_sprite
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
        self.health = 3
        self.last_jump = 0  # The time when the player last jumped
        self.alcohol_consumed = 0  # The number of times you've drunk alcohol
        self.jaundiced = False  # Whether or not the player has jaundice
        self.has_moved = False
        self.final_pos = [0, 0]  # Used to determine where to freeze the frame in the end cutscene
        super().__init__(name, **kwargs)

    def check_jaundice(self):
        if self.alcohol_consumed >= 3:
            self.jaundiced = True
        else:
            self.jaundiced = False

        if self.jaundiced:
            self.max_vel = 3.5
            self.animations = henry_animations_jaundice
            self.animation = self.animations["DEFAULT"]
            return True
        else:
            self.max_vel = 5
            self.animations = henry_animations
            self.animation = self.animations["DEFAULT"]
            return False


class Enemy(Entity):
    def __init__(self, name, **kwargs):
        self.movespeed = 4.5
        self.last_player_collision = 0  # Used to determine collision specifically with the player
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


class Powerup(Entity):
    def __init__(self, name, **kwargs):
        self.powerup_type = ""
        super().__init__(name, **kwargs)
        self.effects = {
            "": self.default_effect,
            "ALCOHOL": self.alcohol_effect,
            "COFFEEBEANS": self.coffee_beans_effect
        }
        self.sprites = {
            "": default_sprite,
            "ALCOHOL": alcohol,
            "COFFEEBEANS": coffeebeans
        }
        self.animation = [self.sprites[self.powerup_type]]
        self.effect = self.effects[self.powerup_type]
        self.hitbox = pygame.Rect((self.pos, (self.animation[0].get_width(), self.animation[0].get_height())))

    @staticmethod
    def default_effect(target):
        print(f"{target.name}, this powerup doesn't have a valid type. You are clearly a fool. Get out of my computer game, imbecile.")

    @staticmethod
    def alcohol_effect(target):
        target.health += 1
        target.alcohol_consumed += 1
        drink.play()

    @staticmethod
    def coffee_beans_effect(target):
        target.alcohol_consumed = 0
        target.health += 1
        target.check_jaundice()
        eat.play()


class FriendlyEntity(Entity):
    def __init__(self, name, **kwargs):
        self.conversed = False  # If you already talked to this entity
        self.conversation = []  # All of the textboxes for the conversation with this entity
        self.conversation_index = 0
        super().__init__(name, **kwargs)

    def check_on_screen(self, entities):  # Checks that this entity is on screen and there are no enemies on screen to initiate conversation
        player = None
        enemies = []
        for entity in entities:
            if type(entity) == Player:
                player = entity
            if type(entity) == Enemy:
                enemies.append(entity)
        if player is not None:
            for enemy in enemies:
                if player.pos[0] + (screen_size[0] + player.hitbox.width) / 2 >= enemy.pos[0] >= player.pos[0] - (screen_size[0] + player.hitbox.width) / 2:
                    return False  # If there are any enemies onscreen, return False
            if player.pos[0] - 250 + (screen_size[0] + player.hitbox.width) / 2 >= self.pos[0] >= player.pos[0] + 250 - (screen_size[0] + player.hitbox.width) / 2:
                return True  # If the entity is onscreen and no enemies are onscreen, return True
        return False  # If the player is dead or is not on the same screen as the entity, return False

    def run_conversation(self):  # Set current_textbox to the output of this function every frame
        try:
            if self.conversation[self.conversation_index].finished:
                self.conversation_index += 1
            return self.conversation[self.conversation_index]
        except IndexError:
            self.conversed = True
            return None


def calculate_score(entities, player):
    enemies = 0
    powerups = 0
    enemies_killed = 17
    powerups_consumed = 6
    for entity in entities:
        if type(entity) == Enemy:
            enemies += 1
        if type(entity) == Powerup:
            powerups += 1
    enemies_killed -= enemies
    powerups_consumed -= powerups
    damage_taken = (3 + powerups_consumed) - player.health
    score = round((enemies_killed + powerups_consumed) / (23 + (damage_taken / 1.5)) * 1000)
    output = f"Enemies killed: {enemies_killed}/17 - Powerups consumed: {powerups_consumed}/6 - Damage taken: {damage_taken} - Total score: {score}/1000"
    return output

