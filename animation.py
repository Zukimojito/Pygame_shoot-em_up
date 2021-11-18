import pygame
import os
from config import *

class Animation :
    def __init__(self):
        
        self.expl_anim = {}
        self.expl_anim['big'] = []
        self.expl_anim['small'] = []
        self.expl_anim['player'] = []

        #Explosion animation
        for i in range(9) :
            self.expl_img = pygame.image.load(os.path.join("Image/Explosion_anim",f"expl{i}.png")).convert()
            self.expl_img.set_colorkey(BLACK)
            self.player_expl_img = pygame.image.load(os.path.join("Image/Player_Explosion_anim",f"player_expl{i}.png")).convert()
            self.player_expl_img.set_colorkey(BLACK)
            self.expl_anim['big'].append(pygame.transform.scale(self.expl_img, (70,70)))
            self.expl_anim['small'].append(pygame.transform.scale(self.expl_img,(25,25)))
            self.expl_anim['player'].append(self.player_expl_img)

class Laser_Animation :
    def __init__(self):
        self.laser_anim = {}
        self.laser_anim['Laser_ult'] = []


        #Laser animation
        for i in range(12) :
            self.laser_img = pygame.image.load(os.path.join("Image/Laser_anim",f"laser{i}.png")).convert()
            self.laser_img = pygame.transform.scale(self.laser_img, (WIN_HEIGHT , 200))
            self.laser_img = pygame.transform.rotate(self.laser_img,90)
            self.laser_img.set_colorkey(BLACK)
            self.laser_anim['Laser_ult'].append(self.laser_img)