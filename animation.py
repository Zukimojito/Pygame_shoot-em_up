import pygame
import os
from config import *

class Animation :
    def __init__(self):
        
        self.expl_anim = {}
        self.expl_anim['big'] = []
        self.expl_anim['small'] = []
        self.expl_anim['player'] = []



        for i in range(9) :
            self.expl_img = pygame.image.load(os.path.join("Image/Explosion_anim",f"expl{i}.png")).convert()
            self.expl_img.set_colorkey(BLACK)
            self.player_expl_img = pygame.image.load(os.path.join("Image/Player_Explosion_anim",f"player_expl{i}.png")).convert()
            self.player_expl_img.set_colorkey(BLACK)
            self.expl_anim['big'].append(pygame.transform.scale(self.expl_img, (70,70)))
            self.expl_anim['small'].append(pygame.transform.scale(self.expl_img,(25,25)))
            self.expl_anim['player'].append(self.player_expl_img)