import pygame
import os

pygame.mixer.init()

Shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
Death_sound = pygame.mixer.Sound(os.path.join("Sound","rumble.ogg"))
Heal_sound = pygame.mixer.Sound(os.path.join("Sound","pow0.wav"))
Boost_sound = pygame.mixer.Sound(os.path.join("Sound","pow1.wav"))
Laser_sound = pygame.mixer.Sound(os.path.join("Sound","laser.mp3"))
Boss1_rire = pygame.mixer.Sound(os.path.join("Sound","rire.mp3"))

explo_sound = [
    pygame.mixer.Sound(os.path.join("Sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("Sound","expl1.wav"))
]
Music_Main = pygame.mixer.music.load(os.path.join("Sound","Swallowed_star_bgm1.mp3"))

pygame.mixer.music.set_volume(0.8)

Shoot_sound.set_volume(0.1)
explo_sound[0].set_volume(0.1)
explo_sound[1].set_volume(0.1)
Heal_sound.set_volume(0.1)
Boost_sound.set_volume(0.1)