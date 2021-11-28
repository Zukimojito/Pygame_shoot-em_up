import pygame
import os

pygame.mixer.init()

Shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
Death_sound = pygame.mixer.Sound(os.path.join("Sound","rumble.ogg"))
Laser_sound = pygame.mixer.Sound(os.path.join("Sound","laser.mp3"))


item_sound = [
    pygame.mixer.Sound(os.path.join("Sound","pow0.wav")),
    pygame.mixer.Sound(os.path.join("Sound","pow1.wav"))
]
explo_sound = [
    pygame.mixer.Sound(os.path.join("Sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("Sound","expl1.wav"))
]
Music_Main = pygame.mixer.music.load(os.path.join("Sound","Swallowed_star_bgm1.mp3"))

pygame.mixer.music.set_volume(0.8)

Shoot_sound.set_volume(0.1)
explo_sound[0].set_volume(0.1)
explo_sound[1].set_volume(0.1)
item_sound[0].set_volume(0.1)
item_sound[1].set_volume(0.1)