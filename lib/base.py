import pygame

screen_size = (1280, 720)

terrain_floor = [
    [-720, 85, 708],
    [86, 781, 160],
    [782, 2044, 326],
    [2045, 2551, 125],
    [2552, 3133, 177],
    [3134, 3499, 57],
    [3500, 3763, 249],
    [3764, 4120, 404],
    [4121, 4686, 320],
    [4687, 5449, 404],
    [5450, 6005, 217],
    [6006, 6604, 251],
    [6605, 7400, 55],
    [7401, 8182, 166],
    [8183, 9443, 263],
    [9444, 10415, 93],
    [10416, 11536, 288],
    [11537, 12710, 151],
    [12711, 14591, 306]
]

pygame.mixer.init()
terrain = pygame.image.load("assets/sprites/terrain.png")
marker = pygame.image.load("assets/sprites/marker.png")
default_sprite = pygame.image.load("assets/sprites/default_sprite.png")
background = pygame.image.load("assets/sprites/basebackground.jpg")

healthbar_text = pygame.image.load("assets/sprites/healthbar_text.png")
heart_empty = pygame.image.load("assets/sprites/heart_empty.png")
heart_full = pygame.image.load("assets/sprites/heart_full.png")

alcohol = pygame.image.load("assets/sprites/alcohol.png")
coffeebeans = pygame.image.load("assets/sprites/coffeebeans.png")

rinaldi = pygame.image.load("assets/sprites/rizz_breen.png")
austrian = pygame.image.load("assets/sprites/austrian.png")

henry = pygame.image.load("assets/sprites/henry.png")
henry_jump = pygame.image.load("assets/sprites/henry_jump.png")
henry_jaundice = pygame.image.load("assets/sprites/henry_jaundice.png")
henry_jump_jaundice = pygame.image.load("assets/sprites/henry_jump_jaundice.png")

boom = pygame.mixer.Sound("assets/sounds/vine_boom.mp3")
riff = pygame.mixer.Sound("assets/sounds/riff.mp3")
jump = pygame.mixer.Sound("assets/sounds/jump.mp3")
drink = pygame.mixer.Sound("assets/sounds/drink.mp3")
eat = pygame.mixer.Sound("assets/sounds/eat.mp3")

jump.set_volume(0.07)
boom.set_volume(0.2)
riff.set_volume(0.25)
drink.set_volume(0.8)
eat.set_volume(0.8)

henry_default_animation = [henry]
henry_jump_animation = [henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_default_animation]
henry_default_animation_jaundice = [henry_jaundice]
henry_jump_animation_jaundice = [henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_jump_jaundice, henry_default_animation_jaundice]

austrian_default_animation = [austrian]

henry_animations = {
    "DEFAULT": henry_default_animation,
    "JUMP": henry_jump_animation
}

henry_animations_jaundice = {
    "DEFAULT": henry_default_animation_jaundice,
    "JUMP": henry_jump_animation_jaundice
}

austrian_animations = {
    "DEFAULT": austrian_default_animation
}
