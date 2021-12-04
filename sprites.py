from typing import final
import pygame
import math
import random
import os
import numpy as np
from config import *
from song import *
from animation import *
from math import cos, sin, pi


class Player(pygame.sprite.Sprite) :
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        #Player_Img = pygame.image.load(os.path.join("Image","player.png")).convert_alpha()      # keep transparency
        self.image = pygame.image.load(os.path.join("Image","player.png"))
        self.image = pygame.transform.scale(self.image,(100,100))
        self.image.set_colorkey(BLACK)     #Remove background BLACK colors 
        #self.image = pygame.Surface((50,35))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
        self.rect.centerx = WIN_WIDTH / 2
        self.rect.bottom = WIN_HEIGHT - 50
        self.speedX = 5
        self.speedY = 4
        self.last = pygame.time.get_ticks()
        self.cooldown = 250
        self.health = 100
        self.mana = 200
        self.live = 3
        self.nb_sbire = 0
        self.boost = 1
        self.boost_time = 0
        self.speed_time = pygame.time.get_ticks()

    def update(self) :
        now = pygame.time.get_ticks()

        if self.boost > 1 and now - self.boost_time > 10000 :
            self.boost -= 1
            self.boost_time = now

        self.movement()
        self.bullet()
        self.stats()

    def movement(self) :
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        #Item speed
        if self.speedX > 10 :
            self.speedX = 10
        if self.speedY > 9 :
            self.speedY = 9

        if self.speedX > 5 and self.speedY > 4 and now - self.speed_time > 5000 :
            self.speed_time = now
            self.speedX -= 1
            self.speedY -= 1

        if keys[pygame.K_LEFT] or keys[pygame.K_q] :
            self.rect.x -= self.speedX

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.rect.x += self.speedX

        if keys[pygame.K_UP] or keys[pygame.K_z] :
            self.rect.y -= self.speedY
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.rect.y += self.speedY

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

        if self.cooldown < 100 :
            self.cooldown = 100

        if not(self.game.LaserIsActive) :
            if keys[pygame.K_j] or keys[pygame.K_SPACE]:
                if self.now - self.last >= self.cooldown:
                    self.last = self.now
                    self.shoot()

    def shoot(self) :

        if self.boost == 1 :
            bullet = Bullet(self.rect.centerx,self.rect.top)
            self.game.all_sprites.add(bullet)
            self.game.Bullets.add(bullet)
            Shoot_sound.play()
        elif self.boost == 2 :
            bullet1 = Bullet(self.rect.left,self.rect.top)
            bullet2 = Bullet(self.rect.right,self.rect.top)
            self.game.all_sprites.add(bullet1)
            self.game.all_sprites.add(bullet2)
            self.game.Bullets.add(bullet1)
            self.game.Bullets.add(bullet2)
            Shoot_sound.play()
        elif self.boost > 2 :
            bullet1 = Bullet(self.rect.left,self.rect.top)
            bullet2 = Bullet(self.rect.right,self.rect.top)
            bullet3 = Bullet(self.rect.centerx, self.rect.top)
            self.game.all_sprites.add(bullet1)
            self.game.all_sprites.add(bullet2)
            self.game.all_sprites.add(bullet3)
            self.game.Bullets.add(bullet1)
            self.game.Bullets.add(bullet2)
            self.game.Bullets.add(bullet3)
            Shoot_sound.play()

    def GunUp(self) :
        self.boost += 1
        self.boost_time = pygame.time.get_tick()

    def stats(self) :
        if self.health > 100 :
            self.health = 100

        if self.mana > 200 :
            self.mana = 200
        elif self.mana < 0 :
            self.mana = 0
"""
    def laser_shoot(self) :
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LCTRL] :
            self.game.LaserIsActive = True
            self.game.all_sprites.add(self.laser)
            self.game.Laser_sprites.add(self.laser)
        else :
            self.game.LaserIsActive = False
            self.laser.kill()
            Laser_sound.stop()"""

class Rock(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        Rock_Imgs = []
        for i in range(0,7) :
            Rock_Imgs.append(pygame.image.load(os.path.join("Image/Rock",f"rock{i}.png")).convert())
        self.image_original = random.choice(Rock_Imgs)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.80 / 2
        #pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
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
        Bullet_Img = pygame.image.load(os.path.join("Image","19.png"))
        #self.image = pygame.transform.scale(Bullet_Img,(10,45))
        self.image = pygame.transform.scale(Bullet_Img,(40,10))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((10,20))
        #self.image.fill(TURQUOISE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = -10

    def update(self) :
        self.player_shoot()

    def player_shoot(self) :
        self.rect.y += self.speedY
        if self.rect.bottom < 0 :
            self.kill()

class Laser(pygame.sprite.Sprite) :
    def __init__(self, game, size) :
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.animation = Laser_Animation()
        self.size = size
        self.image = self.animation.laser_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    #For key_pressed
    def update(self) :
        now = pygame.time.get_ticks()

        self.rect.centerx = self.game.player.rect.centerx
        self.rect.bottom = self.game.player.rect.top - 25

        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.animation.laser_anim[self.size]) :
                self.frame = 0
            else :
                self.image = self.animation.laser_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
    """
    #For one click 
    def update(self) :
        now = pygame.time.get_ticks()

        self.rect.centerx = self.game.player.rect.centerx
        self.rect.bottom = self.game.player.rect.top - 25

        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.animation.laser_anim[self.size]) :
                self.kill()
                self.game.LaserIsActive = False
                Laser_sound.stop()
            else :
                self.image = self.animation.laser_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center"""

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

class Boss2(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","boss2.png"))
        self.image.set_colorkey((0, 0, 0))
        self.org_image = self.image.copy()
        self.game = game
        self.angle = 0
        self.direction1 = pygame.Vector2(0, 0)
        self.direction = []
        self.rect = self.image.get_rect(center=(WIN_WIDTH / 2, -100))
        self.pos = pygame.Vector2(self.rect.center)
        self.health = 1000
        self.cooldown = 300
        self.last_time = pygame.time.get_ticks()
        self.random_rotate = random.randint(-90,90)
        self.speed = 3
        self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
        self.position_y = random.randint(0,(WIN_HEIGHT - self.rect.height - 300))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > self.cooldown :
            self.last_time = now
            
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_o]:
            self.angle += 3
        if pressed[pygame.K_u]:
            self.angle -= 3
        
        self.direction1 = pygame.Vector2(0, 1).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.movement()
        self.rotate()
        self.kill_self()
    
    def movement(self) :

        if self.rect.top < 0 :
            self.rect.y += 1
        else :
            if self.rect.x < self.position_x :
                self.rect.x += self.speed
            elif self.rect.x > self.position_x :
                self.rect.x -= self.speed
            if self.rect.y < self.position_y :
                self.rect.y += self.speed
            elif self.rect.y > self.position_y :
                self.rect.y -= self.speed

            if abs(self.rect.x - self.position_x) < self.speed/2 :
                self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
                self.shoot()
                
            if abs(self.rect.y - self.position_y) < self.speed/2 :
                self.position_y = random.randint(0,(WIN_HEIGHT - self.rect.height - 300))
                self.shoot()

    def rotate(self) :
        if self.rect.top < 0 :
            pass
        else :
            if self.angle < self.random_rotate :
                self.angle += 2
            elif self.angle > self.random_rotate :
                self.angle -= 2

            if abs(self.angle - self.random_rotate) < self.speed/2 :
                self.random_rotate = random.randint(-180,180)
                self.shoot()

    def final_shot(self) :
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(i, 1).rotate(-self.angle))             #angle 270° ~ 315°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(1, i).rotate(-self.angle))             #angle 315° ~ 360°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(1, -i).rotate(-self.angle))            #angle 0° ~ 45°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(i, -1).rotate(-self.angle))            #angle 45° ~ 90°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-i, -1).rotate(-self.angle))           #angle 90° ~ 135°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-1, -i).rotate(-self.angle))           #angle 135° ~ 180°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-1, i).rotate(-self.angle))            #angle 180° ~ 225°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-i, 1).rotate(-self.angle))            #angle 180° ~ 225°
            
        final_shoot = []
        for i in range(40) :
            final_shoot.append(Projectile_Boss(self.rect.center, self.direction[i]))
            #self.groups()[0].add(final_shoot)
            self.game.all_sprites.add(final_shoot)
            self.game.Bullets_boss.add(final_shoot)

        """
        shoot1 = Projectile(self.rect.center, self.direction1)
        self.groups()[0].add(shoot1)
        """
    
    def shoot(self) :
        """
        shoot = Bullet_Boss(self.rect.centerx, self.rect.bottom)
        self.groups()[0].add(shoot)
        self.game.Bullets_boss.add(shoot)"""

        shoot = Bullet_Boss_auto_direction(self.rect.center , self.direction1, self.angle)
        self.groups()[0].add(shoot)
        self.game.Bullets_boss.add(shoot)

    def kill_self(self) :
        if self.health < 1 :
            self.game.Boss2_IsAlive = False
            self.kill()

class Boss1(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","boss1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(256,232))
        self.image.set_colorkey((0, 0, 0))
        self.org_image = self.image.copy()
        self.game = game
        self.angle = 0
        self.direction = []
        self.rect = self.image.get_rect(center=(WIN_WIDTH / 2, -200))
        self.pos = pygame.Vector2(self.rect.center)
        self.health = 1000
        self.cooldown = 300
        self.last_time = pygame.time.get_ticks()
        self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
        self.position_y = random.randint(0,(WIN_HEIGHT - self.rect.height - 100))
        self.speed = 3

    def update(self):
        """
        now = pygame.time.get_ticks()
        if now - self.last_time > self.cooldown :
            self.last_time = now
            self.shoot()"""

        self.movement()
        self.kill_self()
    
    def movement(self) :

        if self.rect.top < 0 :
            self.rect.y += 1
        else : 
            if self.rect.x < self.position_x :
                self.rect.x += self.speed
            elif self.rect.x > self.position_x :
                self.rect.x -= self.speed
            if self.rect.y < self.position_y :
                self.rect.y += self.speed
            elif self.rect.y > self.position_y :
                self.rect.y -= self.speed

            if abs(self.rect.x - self.position_x) < self.speed/2 :
                self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
                self.shoot()
                
            if abs(self.rect.y - self.position_y) < self.speed/2 :
                self.position_y = random.randint(0,(WIN_HEIGHT - self.rect.height - 100))
                self.shoot()

    def final_shot(self) :
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(i, 1).rotate(-self.angle))             #angle 270° ~ 315°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(1, i).rotate(-self.angle))             #angle 315° ~ 360°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(1, -i).rotate(-self.angle))            #angle 0° ~ 45°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(i, -1).rotate(-self.angle))            #angle 45° ~ 90°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-i, -1).rotate(-self.angle))           #angle 90° ~ 135°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-1, -i).rotate(-self.angle))           #angle 135° ~ 180°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-1, i).rotate(-self.angle))            #angle 180° ~ 225°
        for i in np.arange(0, 1.25, 0.25) :
            self.direction.append(pygame.Vector2(-i, 1).rotate(-self.angle))            #angle 180° ~ 225°
            
        final_shoot = []
        for i in range(40) :
            final_shoot.append(Projectile_Boss(self.rect.center, self.direction[i]))
            self.game.all_sprites.add(final_shoot)
            self.game.Bullets_boss.add(final_shoot)
        """
        shoot1 = Projectile(self.rect.center, self.direction1)
        self.groups()[0].add(shoot1)
        """
    
    def shoot(self) :
        
        shoot1 = Bullet_Boss(self.rect.centerx - 37, self.rect.centery + 150 )
        shoot2 = Bullet_Boss(self.rect.centerx + 37, self.rect.centery + 150 )
        self.groups()[0].add(shoot1)
        self.groups()[0].add(shoot2)
        self.game.Bullets_boss.add(shoot1)
        self.game.Bullets_boss.add(shoot2)

        """
        shoot = Bullet_Boss_auto_direction((self.rect.centerx - 37, self.rect.centery + 130) , self.direction1, self.angle)
        self.groups()[0].add(shoot)
        self.game.Bullets_boss.add(shoot)

        shoot1 = Bullet_Boss_auto_direction((self.rect.centerx + 37, self.rect.centery + 130) , self.direction1, self.angle)
        self.groups()[0].add(shoot1)
        self.game.Bullets_boss.add(shoot1)"""
        
    def kill_self(self) :
        if self.health < 1 :
            self.game.Boss1_IsAlive = False
            self.kill()

class Bullet_Boss(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","11.png"))
        self.image = pygame.transform.scale(self.image,(40,10))
        self.image = pygame.transform.rotate(self.image,-90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = -8
        self.speedX = 10

    def update(self) :
        self.shoot()

    def shoot(self) :
        self.rect.y -= self.speedY
        if self.rect.top > WIN_HEIGHT or self.rect.bottom < 0 or self.rect.right > WIN_WIDTH or self.rect.left < 0 :
            self.kill()

class Projectile_Boss(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","balls.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(16,15))
        self.image = pygame.transform.rotate(self.image,-90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 5

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

class Bullet_Boss_auto_direction(pygame.sprite.Sprite):
    def __init__(self, pos, direction, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","14.png"))
        self.image = pygame.transform.scale(self.image,(40,10))
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.rotate(self.image, angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=pos)
        #self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.direction = direction.normalize()
        self.pos = pygame.Vector2(self.rect.center)

        self.speed = 5

    def update(self):
        self.pos += self.direction * self.speed
        #self.pos = (self.pos[0] + self.speed*self.direction[0], self.pos[1] + self.speed*self.direction[1])
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

class Item(pygame.sprite.Sprite) :
    def __init__(self, center) :
        pygame.sprite.Sprite.__init__(self)
        item_drop = {}
        item_drop['potion'] = pygame.image.load(os.path.join("Image/Item","potion.png"))
        item_drop['sbire'] = pygame.image.load(os.path.join("Image/Item","sbire.png"))
        item_drop['speed'] = pygame.image.load(os.path.join("Image/item","milkway.png"))
        item_drop['boost'] = pygame.image.load(os.path.join("Image/Item","trollpng.png"))
        #item_drop['dio'] = pygame.image.load(os.path.join("Image/Item","dio.png"))
        self.type = random.choice(['potion','sbire','speed','boost'])
        self.image = item_drop[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = center)
        self.speedy = 5
    
    def update(self) :
        self.movement()
        self.self_kill()
    
    def movement(self) :
        self.rect.y += self.speedy

    def self_kill(self) :
        if self.rect.top > WIN_HEIGHT :
            self.kill()

class Sbire(pygame.sprite.Sprite) :
    def __init__(self, game) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Image","sbire.png"))
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIN_WIDTH - self.rect.width)
        self.rect.bottom = WIN_HEIGHT - 50
        self.cooldown = 250
        self.speedX = 4
        self.speedY = 3
        self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
        self.position_y = random.randint(400,(WIN_HEIGHT - self.rect.height - 100))
    
    def update(self) :
        self.movement()
        self.self_kill()
    
    def movement(self) :
        if self.rect.x < self.position_x :
            self.rect.x += self.speedX
        elif self.rect.x > self.position_x :
            self.rect.x -= self.speedX
        if self.rect.y < self.position_y :
            self.rect.y += self.speedY
        elif self.rect.y > self.position_y :
            self.rect.y -= self.speedY

        if abs(self.rect.x - self.position_x) < self.speedX :
            self.position_x = random.randint(0,(WIN_WIDTH - self.rect.width))
            self.shoot()
                
        if abs(self.rect.y - self.position_y) < self.speedY :
            self.position_y = random.randint(400 ,(WIN_HEIGHT - self.rect.height - 100))
            self.shoot()

    def shoot(self) :
        bullet = Bullet(self.rect.centerx,self.rect.top)
        self.game.all_sprites.add(bullet)
        self.game.Bullets.add(bullet)
        Shoot_sound.play()

    def self_kill(self) :
        pass

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


    

