import pygame
import os

def load_booster(BOOSTER_SIZE):
    #LOAD IMAGES AND SCALE
    HEART = pygame.image.load(
        os.path.join("Assets", "heart.png"))
    HEART_IMAGE = pygame.transform.scale(
        HEART, (BOOSTER_SIZE, BOOSTER_SIZE))
    ROCKET = pygame.image.load(
        os.path.join("Assets", "rocket.png"))
    ROCKET_IMAGE = pygame.transform.scale(
        ROCKET, (BOOSTER_SIZE, BOOSTER_SIZE))
    SNIPER = pygame.image.load(
        os.path.join("Assets", "sniper.png"))
    SNIPER_IMAGE = pygame.transform.scale(
        SNIPER, (BOOSTER_SIZE, BOOSTER_SIZE))
    CANNON = pygame.image.load(
        os.path.join("Assets", "cannon.png"))
    CANNON_IMAGE = pygame.transform.scale(
        CANNON, (BOOSTER_SIZE, BOOSTER_SIZE))
    SONIC = pygame.image.load(
        os.path.join("Assets", "sonic.png"))
    SONIC_IMAGE = pygame.transform.scale(
        SONIC, (BOOSTER_SIZE, BOOSTER_SIZE))
    
    return HEART_IMAGE, ROCKET_IMAGE, SNIPER_IMAGE, CANNON_IMAGE, SONIC_IMAGE

    