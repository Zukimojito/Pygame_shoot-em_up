import pygame
import math
import random
import os

from pygame.constants import MOUSEBUTTONUP
from config import *
from sprites import Button

class Draw_screen :
    def __init__(self, game) :
        self.game = game
        self.Player_Lives_Img = pygame.image.load(os.path.join("Image","player.png")).convert_alpha()
        self.Player_Lives_Img = pygame.transform.scale(self.Player_Lives_Img,(25,25))
        self.Sbire_Lives_Img = pygame.image.load(os.path.join("Image","sbire.png")).convert_alpha()
        self.Sbire_Lives_Img = pygame.transform.scale(self.Sbire_Lives_Img,(25,25))
        #self.Player_Lives_Img.set_colorkey(WHITE)
        self.Background_Img_Menu = pygame.image.load(os.path.join("Image","Background1.jpg"))
        self.Background_Img_GameOver = pygame.image.load(os.path.join("Image","end.png"))

    def Draw_score(self, surf, text, size, x, y) :
        font = pygame.font.Font(self.game.font ,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def Draw_health(self, surf, hp, x, y) :
        if hp < 0 :
            hp = 0
        if hp > 100 :
            hp = 100
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp/100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 1)

    def Draw_Mana(self, surf, mp, x, y) :
        if mp < 0 :
            mp = 0
        if mp > 200 :
            mp = 200
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (mp/200) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill,  BAR_HEIGHT)
        pygame.draw.rect(surf, PURPLE, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 1)
    
    def Draw_live(self, surf, lives, img, x, y) :
        for i in range(lives) :
            img_rect = img.get_rect()
            img_rect.x = x + 30*i
            img_rect.y = y
            surf.blit(img,img_rect)

    def Draw_sbire(self, surf, number, img, x, y) :
        for i in range(number) :
            img_rect = img.get_rect()
            img_rect.x = x + 30*i
            img_rect.y = y
            surf.blit(img,img_rect)


    def draw_text(self, surf, text, size, x, y) :
        font = pygame.font.Font(self.game.font ,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def Draw_init(self) :
        self.game.screen.blit(self.Background_Img_Menu,(0,0))
        self.draw_text(self.game.screen,'Swallowed Star', 64, WIN_WIDTH/2, WIN_HEIGHT/4)
        self.draw_text(self.game.screen,'Press ↑ ↓ ← or → to move', 28, WIN_WIDTH/2, WIN_HEIGHT/2 - 100)
        self.draw_text(self.game.screen,'Press SPACE to shoot', 28, WIN_WIDTH/2, WIN_HEIGHT/1.75 - 100)
        self.draw_text(self.game.screen,'Press Ctrl to ult', 28, WIN_WIDTH/2, WIN_HEIGHT/1.75 - 50)
        self.draw_text(self.game.screen,'Press C to summoner', 28, WIN_WIDTH/2, WIN_HEIGHT/1.75)
        self.draw_text(self.game.screen,'by Zukimojito', 12, WIN_WIDTH/1.075, WIN_HEIGHT-20)

        Play_Button = Button(WIN_WIDTH/2, WIN_HEIGHT/1.25, 150, 50, WHITE, BLACK, 'Play', 32)

        self.waiting = True
        while self.waiting :
            for event in pygame.event.get() :
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                
                if event.type == pygame.QUIT :
                    pygame.quit()
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if Play_Button.Is_Pressed(mouse_pos, mouse_pressed) :
                        self.waiting = False
                        return False
                """
                elif event.type == pygame.KEYUP :
                    self.waiting = False
                    return False"""

            """
            if Play_Button.Is_Pressed(mouse_pos, mouse_pressed) :
                self.waiting = False
                return False"""
            self.game.screen.blit(Play_Button.image, Play_Button.rect)
            self.game.clock.tick(FPS)
            pygame.display.update()