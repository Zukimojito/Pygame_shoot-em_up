import pygame
import math
import random
import os
from pygame import draw

from pygame.constants import MOUSEBUTTONUP
from config import *


class Button() :
    def __init__(self, x, y, width, height, fg, bg, content, fontsize) :
        self.font = pygame.font.Font(os.path.join("Text","font.ttf"),fontsize)
        self.content = content

        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        ##self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))

        self.image.blit(self.text, self.text_rect)

    def Is_Pressed(self, pos, pressed) :
        if self.rect.collidepoint(pos) :
            if pressed[0] :
                return True
            return False
        return False

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
        self.level = []

    def Draw_score(self, surf, text, size, x, y) :
        font = pygame.font.Font(self.game.font ,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)
    
    def Draw_dps(self, surf, text, size, x, y) :
        self.draw_text(self.game.screen,'dps/ball', 20, WIN_WIDTH - 50,WIN_HEIGHT-25)
        font = pygame.font.Font(self.game.font ,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def Draw_health(self, surf, hp, x, y) :
        if hp < 0 :
            hp = 0
        if hp > self.game.player.max_health :
            hp = self.game.player.max_health
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp/self.game.player.max_health) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 1)
    
    def Draw_health_boss1(self, surf, hp, x, y) :
        BAR_LENGTH = 10
        BAR_HEIGHT = 100
        fill = (hp/self.game.boss1.max_health) * BAR_HEIGHT
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, BAR_LENGTH, fill)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, RED, outline_rect, 1)
    
    def Draw_health_boss2(self, surf, hp, x, y) :
        BAR_LENGTH = 10
        BAR_HEIGHT = 100
        fill = (hp/self.game.boss2.max_health) * BAR_HEIGHT
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, BAR_LENGTH, fill)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, RED, outline_rect, 1)


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
    
    def Rank(self) : 

        self.level = ['地球人','学徒级','行星级','恒星级','宇宙级','域主级','界主级','不朽级','宇宙尊者','宇宙之主','真神','虚空真神','永恒真神','混沌主宰','神王级','领主级']
        self.draw_text(self.game.screen,'Your Rank : ', 64, WIN_WIDTH/2 - 100, WIN_HEIGHT/1.9)

        
        if self.game.score >= 0 and self.game.score < 100 :
            self.draw_text(self.game.screen,self.level[0], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 100 and self.game.score < 500 :
            self.draw_text(self.game.screen,self.level[1], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 500 and self.game.score < 1000 :
            self.draw_text(self.game.screen,self.level[2], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 1000 and self.game.score < 2000 :
            self.draw_text(self.game.screen,self.level[3], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 2000 and self.game.score < 5000 :
            self.draw_text(self.game.screen,self.level[4], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 5000 and self.game.score < 7500 :
            self.draw_text(self.game.screen,self.level[5], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 7500 and self.game.score < 10000 :
            self.draw_text(self.game.screen,self.level[6], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 10000 and self.game.score < 15000 :
            self.draw_text(self.game.screen,self.level[7], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 15000 and self.game.score < 20000 :
            self.draw_text(self.game.screen,self.level[8], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 20000 and self.game.score < 30000 :
            self.draw_text(self.game.screen,self.level[9], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 30000 and self.game.score < 40000 :
            self.draw_text(self.game.screen,self.level[10], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 40000 and self.game.score < 50000 :
            self.draw_text(self.game.screen,self.level[11], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 50000 and self.game.score < 75000 :
            self.draw_text(self.game.screen,self.level[12], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 75000 and self.game.score < 100000 :
            self.draw_text(self.game.screen,self.level[13], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 100000 and self.game.score < 500000 :
            self.draw_text(self.game.screen,self.level[14], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)
        if self.game.score >= 500000 :
            self.draw_text(self.game.screen,self.level[15], 64, WIN_WIDTH/2 + 185, WIN_HEIGHT/1.9)