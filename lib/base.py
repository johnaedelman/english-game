import pygame

screen_size = (1280, 720)

terrain_floor = [
    [0, 540, 200],  # Lower bound on x-axis, upper bound on x-axis, y-value to set as floor
    [541, 1080, 400]
]

pygame.mixer.init()
terrain = pygame.image.load("assets/sprites/terrain.png")
marker = pygame.image.load("assets/sprites/marker.png")
healthbar_text = pygame.image.load("assets/sprites/healthbar_text.png")
heart_empty = pygame.image.load("assets/sprites/heart_empty.png")
heart_full = pygame.image.load("assets/sprites/heart_full.png")

henry = pygame.image.load("assets/sprites/henry.png")
henry_jump = pygame.image.load("assets/sprites/henry_jump.png")

augh = pygame.mixer.Sound("assets/sounds/augh.mp3")
boom = pygame.mixer.Sound("assets/sounds/vine_boom.mp3")
riff = pygame.mixer.Sound("assets/sounds/riff.mp3")
jump = pygame.mixer.Sound("assets/sounds/jump.mp3")

jump.set_volume(0.07)
boom.set_volume(0.2)
riff.set_volume(0.25)

henry_default_animation = [henry]
henry_jump_animation = [henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_jump, henry_default_animation]
