import pygame
import math
import random
import os
from config import *
from song import *
from animation import *


class Player(pygame.sprite.Sprite) :
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        #Player_Img = pygame.image.load(os.path.join("Image","player.png")).convert_alpha()      # keep transparency
        Player_Img = pygame.image.load(os.path.join("Image","player.png")).convert()
        self.image = pygame.transform.scale(Player_Img,(40,25))
        self.image.set_colorkey(BLACK)     #Remove background BLACK colors 
        #self.image = pygame.Surface((50,35))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
        self.rect.centerx = WIN_WIDTH / 2
        self.rect.bottom = WIN_HEIGHT - 50
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.health = 100
        self.live = 3

    def update(self) :

        self.movement()
        self.bullet()

    def movement(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q] :
            self.rect.x -= speedX

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.rect.x += speedX

        if keys[pygame.K_UP] or keys[pygame.K_z] :
            self.rect.y -= speedY
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.rect.y += speedY

        if self.rect.right > WIN_WIDTH :
            self.rect.right = WIN_WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT :
            self.rect.bottom = WIN_HEIGHT
    
    def bullet(self) :
        keys = pygame.key.get_pressed()

        self.now = pygame.time.get_ticks()
        
        if keys[pygame.K_j] or keys[pygame.K_SPACE]:
            if self.now - self.last >= self.cooldown:
                self.last = self.now
                self.shoot()

    def shoot(self) :
        bullet = Bullet(self.rect.centerx,self.rect.top)
        self.game.all_sprites.add(bullet)
        self.game.Bullets.add(bullet)
        Shoot_sound.play()
        #return bullet

class Rock(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        Rock_Imgs = []
        for i in range(0,7) :
            Rock_Imgs.append(pygame.image.load(os.path.join("Image",f"rock{i}.png")).convert())
        self.image_original = random.choice(Rock_Imgs)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
        self.rect.x = random.randrange(0,WIN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedX = random.randrange(-3,3)
        self.speedY = random.randrange(3,6)
        self.rotation_degree = random.randrange(-10,10)
        self.total_rotation_degree = 0

    def update(self) :
        self.rotation()
        self.rect.y += self.speedY
        self.rect.x += self.speedX

        if self.rect.left > WIN_WIDTH or self.rect.right < 0 or self.rect.top > WIN_HEIGHT :
            self.rect.x = random.randrange(0,WIN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-50,-20)
            self.speedX = random.randrange(-3,3)
            self.speedY = random.randrange(3,8)

    def rotation(self) :
        self.total_rotation_degree += self.rotation_degree
        self.total_rotation_degree = self.total_rotation_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_rotation_degree)       #function to rotate
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

class Bullet(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        Bullet_Img = pygame.image.load(os.path.join("Image","bullet.png")).convert()
        self.image = pygame.transform.scale(Bullet_Img,(10,45))
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((10,20))
        #self.image.fill(TURQUOISE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = -10

    def update(self) :
        self.rect.y += self.speedY
        if self.rect.bottom < 0 :
            self.kill()

class Explosion(pygame.sprite.Sprite) :
    def __init__(self, center, size) :
        pygame.sprite.Sprite.__init__(self)
        self.animation = Animation()
        self.size = size
        self.image = self.animation.expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self) :
        now = pygame.time.get_ticks()

        if now - self.last_update > self.frame_rate :                       #every 0.05 sec, we change the next image
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.animation.expl_anim[self.size]) :     #if frame == last image of explo_anim
                #print(f"{len(self.animation.expl_anim[self.size])} FPS")
                self.kill()
            else :
                self.image = self.animation.expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
