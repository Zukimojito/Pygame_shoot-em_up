import pygame
import os
import sys
from sprites import *
from config import *
from draw_texte import *
from song import *

class Game : 
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))       
        self.NameGame = pygame.display.set_caption("Swallowed Star")        #Screen Name
        self.icon = pygame.display.set_icon(pygame.image.load(os.path.join("Image","icon.jpg")))
        self.clock = pygame.time.Clock()                            #Framerate
        self.font = os.path.join("Text","font.ttf")
        self.running = True
        self.show_init = True
        self.Background_Img = pygame.image.load(os.path.join("Image","Background3.jpg")).convert()
        self.Background = pygame.transform.scale(self.Background_Img,(845,800))
        self.Background_Y = 0
        self.score = 0
        self.score_max = 500
        self.draw_screen = Draw_screen(self)
        self.hidden = False
        self.hide_time = 0
        self.Boss1_IsAlive = False
        self.Boss2_IsAlive = False
        self.last_time_boss = pygame.time.get_ticks()
        self.LaserIsActive = False
        self.cooldown_anim_boss1 = pygame.time.get_ticks()
        self.cooldown_anim_boss2 = pygame.time.get_ticks()
        self.laser = Laser(self,'Laser_ult')
        self.maximum_sbire = 0

    def hide(self) :
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.player.kill()

    def new_game(self) :
        #A New game starts
        pygame.mixer.music.play(-1)
        
        self.all_sprites = pygame.sprite.Group()            
        self.Rocks = pygame.sprite.Group()                  #Rock
        self.Bullets = pygame.sprite.Group()                #Bullets player
        self.Items = pygame.sprite.Group()                  #Items
        self.the_boss = pygame.sprite.Group()               #The boss
        self.Bullets_boss = pygame.sprite.Group()           #Bullets Boss
        self.Laser_sprites = pygame.sprite.Group()          #Laser
        self.Allies = pygame.sprite.Group()                 #Sbire
        
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        self.sbire = Sbire(self)
        for i in range(0,5) :
            self.new_rock()
        self.score = 0
        #self.new_boss2()
        self.new_boss1()

    def new_rock(self) : 
        self.rock = Rock()
        self.all_sprites.add(self.rock)
        self.Rocks.add(self.rock)

    def new_boss1(self) :
        self.Boss1_IsAlive = True
        self.boss1 = Boss1(self)
        self.all_sprites.add(self.boss1)
        self.the_boss.add(self.boss1)
        #Boss1_rire.play()

    def new_boss2(self) :
    
        self.Boss2_IsAlive = True
        self.boss2 = Boss2(self)
        self.all_sprites.add(self.boss2)
        self.the_boss.add(self.boss2)
    
    def new_sbire(self) :
        self.sbire = Sbire(self)
        self.all_sprites.add(self.sbire)
        self.Allies.add(self.sbire)
    
    def new_player(self) :
        self.hidden = False
        self.all_sprites.add(self.player)
        self.player.rect.centerx = WIN_WIDTH / 2
        self.player.rect.bottom = WIN_HEIGHT - 50

    def events(self) :

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.running = False
            
            elif event.type == pygame.KEYDOWN :                                             #Press some key Down
                if event.key == pygame.K_SPACE :                                            #Press SPACE                                                
                    #self.player.shoot()                                                    #Player Shoot
                    pass
                if event.key == pygame.K_LCTRL:
                    if self.player.mana > 0 :
                        Laser_sound.play(-1)
                if event.key == pygame.K_c :
                    if self.player.nb_sbire > 0 and self.maximum_sbire < 5:
                        self.new_sbire()
                        self.player.nb_sbire -= 1
                        self.maximum_sbire += 1
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LCTRL] :
            self.player.mana -= 1
            if self.player.mana > 0 :
                self.LaserIsActive = True
                self.all_sprites.add(self.laser)
                self.Laser_sprites.add(self.laser)
            else :
                self.LaserIsActive = False
                self.laser.kill()
                Laser_sound.stop()
        else :
            self.LaserIsActive = False
            self.laser.kill()
            Laser_sound.stop()

    def update(self) :
        self.all_sprites.update()
        now = pygame.time.get_ticks()

        if self.score > self.score_max :                                                    #Spawn the boss
            while not(self.Boss2_IsAlive) :
                self.new_boss2()
                self.score_max += 1000
                break
        
        if now - self.last_time_boss > 60000 :                                               #Spawn the boss1 every 60 sec
            self.last_time_boss = now

            while not(self.Boss1_IsAlive) :
                self.new_boss1()
                break
        
        if self.hidden and now - self.hide_time > 1500 :                                    #after 1.5 s we spawn player
            self.new_player()

        if self.player.live == 0 and not(self.death_expl.alive()):                          #Game over 
            self.show_init = True

    def Collision(self) :
        now = pygame.time.get_ticks()

        #Rock and Bullets
        hits1 = pygame.sprite.groupcollide(self.Rocks, self.Bullets, True, True)             #Collision between Rock and Bullet, if they collide so we delete
        for i in hits1 :
            explo = Explosion(i.rect.center, 'big')
            self.all_sprites.add(explo)
            self.score += int(i.radius)
            random.choice(explo_sound).play()
            self.new_rock()
            self.player.mana += 5
            #Item 
            if random.random() > 0.2 :
                item = Item(i.rect.center)
                self.all_sprites.add(item)
                self.Items.add(item)

        #Player and Rock
        if not(self.hidden) :                                                                   #activate collision by checking if player still has health
            hits2 = pygame.sprite.spritecollide(self.player, self.Rocks, True, pygame.sprite.collide_circle)
            for i in hits2 :
                self.new_rock()
                explo = Explosion(i.rect.center, 'small')
                self.all_sprites.add(explo)
                self.player.health -= int(i.radius)
                if self.player.health < 1 :
                    self.death_expl = Explosion(i.rect.center, 'player')
                    self.all_sprites.add(self.death_expl)
                    Death_sound.play()
                    self.player.live -= 1
                    self.player.health = 100
                    self.hide()
        
        #Boss2 and Bullet_player
        if self.Boss2_IsAlive :                                                          #activate collision by checking if boss still has health
            hits3 = pygame.sprite.spritecollide(self.boss2, self.Bullets, True, pygame.sprite.collide_mask)
            for i in hits3 :
                explo = Explosion(i.rect.center, 'big')
                self.all_sprites.add(explo)
                random.choice(explo_sound).play()
                self.boss2.health -= 10
                if self.boss2.health < 1 :
                    self.boss2.final_shot()
                    explo = Explosion(i.rect.center, 'player')
                    self.all_sprites.add(explo)
        
        #Boss1 and Bullet_player
        if self.Boss1_IsAlive :
            hit6 = pygame.sprite.spritecollide(self.boss1, self.Bullets, True, pygame.sprite.collide_mask)
            for i in hit6 :
                explo = Explosion(i.rect.center, 'big')
                self.all_sprites.add(explo)
                self.boss1.health -= 10
                self.score += 10
                random.choice(explo_sound).play()
                if self.boss1.health < 1 :
                    explo = Explosion(i.rect.center, 'player')
                    self.all_sprites.add(explo)
                    self.boss1.final_shot()

        
        #Bullet_player and Bullet_Boss2
        hit4 = pygame.sprite.groupcollide(self.Bullets, self.Bullets_boss, True, True)
        for i in hit4 :
            explo = Explosion(i.rect.center, 'small')
            self.all_sprites.add(explo)
            random.choice(explo_sound).play()
        
        #Player and Bullet_Boss2
        if not(self.hidden) :        #if player hasn't die
            hit5 = pygame.sprite.spritecollide(self.player, self.Bullets_boss, True, pygame.sprite.collide_mask)
            for i in hit5 :
                explo = Explosion(i.rect.center, 'small')
                self.all_sprites.add(explo)
                self.player.health -= int(random.randrange(5,20))
                random.choice(explo_sound).play()
                if self.player.health < 1 :
                    self.death_expl = Explosion(i.rect.center, 'player')
                    self.all_sprites.add(self.death_expl)
                    Death_sound.play()
                    self.player.live -= 1
                    self.player.health = 100
                    self.hide()

        #Player and Boss1, Boss2
        if not(self.hidden) :
            hit7 = pygame.sprite.spritecollide(self.player, self.the_boss, False, pygame.sprite.collide_mask)
            for i in hit7 :
                self.player.health -= 101
                if self.player.health < 1 :
                    self.death_expl = Explosion(self.player.rect.center, 'player')
                    self.all_sprites.add(self.death_expl)
                    Death_sound.play()
                    self.player.live -= 1
                    self.player.health = 100
                    self.hide()

        #Laser and Rock
        if self.LaserIsActive :
            hit8 = pygame.sprite.spritecollide(self.laser, self.Rocks, True, pygame.sprite.collide_mask)
            for i in hit8 :
                explo = Explosion(i.rect.center, 'big')
                self.all_sprites.add(explo)
                self.score += int(i.radius)
                random.choice(explo_sound).play()
                self.new_rock()

        #Laser and Bullet_boss
        if self.LaserIsActive :
            hit9 = pygame.sprite.spritecollide(self.laser, self.Bullets_boss, True, pygame.sprite.collide_mask)
            for i in hit9 :
                explo = Explosion(i.rect.center, 'small')
                self.all_sprites.add(explo)
                random.choice(explo_sound).play()

        #Laser and Boss2
        if self.Boss2_IsAlive  :
            if self.LaserIsActive :                                                          
                self.hits10 = pygame.sprite.spritecollide(self.laser, self.the_boss, False, pygame.sprite.collide_mask)
                for i in self.hits10 :
                    if now - self.cooldown_anim_boss2 > 200 :
                        self.cooldown_anim_boss2 = now
                        explo = Explosion(i.rect.center, 'big')
                        self.all_sprites.add(explo)
                        random.choice(explo_sound).play()
                        self.boss2.health -= 10
                    if not(self.Boss2_IsAlive) :
                        self.boss2.final_shot()

        #Laser and Boss1
        if self.Boss1_IsAlive :
            if self.LaserIsActive :                                                          
                self.hits11 = pygame.sprite.spritecollide(self.laser, self.the_boss, False, pygame.sprite.collide_mask)
                for i in self.hits11 :
                    if now - self.cooldown_anim_boss1 > 200 :
                        self.cooldown_anim_boss1 = now
                        explo = Explosion(i.rect.center, 'big')
                        self.all_sprites.add(explo)
                        random.choice(explo_sound).play()
                        self.boss1.health -= 10
                    if not(self.Boss1_IsAlive):
                        self.boss1.final_shot()
        
        #Player and Item
        hits12 = pygame.sprite.spritecollide(self.player, self.Items, True, pygame.sprite.collide_mask)
        for i in hits12 :
            if i.type == 'potion' :
                self.player.health += random.randint(10,30)
                random.choice(item_sound).play()
            if i.type == 'sbire' :
                if self.player.nb_sbire < 5 :
                    self.player.nb_sbire += 1
                random.choice(item_sound).play()
            if i.type == 'speed' :
                self.player.speedX += 1
                self.player.speedY += 1
                self.player.cooldown -= 5
                random.choice(item_sound).play()
            if i.type == 'boost' :
                self.player.boost += 1
                random.choice(item_sound).play()

        #Sbire and Rock
        hits13 = pygame.sprite.groupcollide(self.Allies, self.Rocks, True, True, pygame.sprite.collide_circle)
        for i in hits13 :
            self.new_rock()
            self.death_expl = Explosion(i.rect.center, 'player')
            self.all_sprites.add(self.death_expl)
            Death_sound.play()
            self.maximum_sbire -= 1
        
        #Sbire and Bullet_Boss2
        hit14 = pygame.sprite.groupcollide(self.Allies, self.Bullets_boss, True, True, pygame.sprite.collide_mask)
        for i in hit14 :
            self.death_expl = Explosion(i.rect.center, 'player')
            self.all_sprites.add(self.death_expl)
            Death_sound.play()
            self.maximum_sbire -= 1

        #Sbire and Boss1, Boss2
        hit15 = pygame.sprite.groupcollide(self.Allies, self.the_boss, True, False, pygame.sprite.collide_mask)
        for i in hit15 :
            self.death_expl = Explosion(i.rect.center, 'player')
            self.all_sprites.add(self.death_expl)
            Death_sound.play()
            self.maximum_sbire -= 1

    def draw(self) :
        self.screen.fill(BLACK)                                                             #Draw the background colors

        Background_X = int(-0.05 * self.player.rect.centerx)                                 #Move the background moving axe X

        self.screen.blit(self.Background,(Background_X,self.Background_Y))                  #Draw the background
        self.screen.blit(self.Background,(Background_X,-WIN_HEIGHT  + self.Background_Y))   #Draw the seconde background
        if self.Background_Y == WIN_HEIGHT :                                                
            self.Background_Y = 0
        self.Background_Y += 1

        self.all_sprites.draw(self.screen)                                                  #Draw all sprites on screen like player, rock, boss, 
        
        self.draw_screen.Draw_score(self.screen, str(self.score), 20, WIN_WIDTH/2, 10)      #Draw Score on center-top screen
        self.draw_screen.Draw_health(self.screen, self.player.health, 5, 10)                #Draw health on screen
        self.draw_screen.Draw_Mana(self.screen, self.player.mana, 5, 20)
        self.draw_screen.Draw_live(self.screen, self.player.live, self.draw_screen.Player_Lives_Img, WIN_WIDTH - 100, 15)           #Draw Lives on screen
        self.draw_screen.Draw_sbire(self.screen, self.player.nb_sbire, self.draw_screen.Sbire_Lives_Img, 0, WIN_HEIGHT - 30)

        self.clock.tick(FPS)                                                                #FPS by sec
        pygame.display.update()                                                             #Draw the screen

    def main(self) :
        self.events()
        self.update()
        self.Collision()
        self.draw()

        print(f"{self.clock.get_fps()} FPS")        #Show FPS in terminal

    def game_over(self) :
        pass

game = Game()

while game.running :                                        #Game running 
    if game.show_init :                                     #Open Main Menu
        close_game = game.draw_screen.Draw_init()
        if close_game :                                     #If we close the game, so break
            break
        else :
            game.show_init = False                          #Else if player start a game so Close Main Menu
            game.new_game()                                 #Add all Sprites 
    game.main()                                             #Game start !!

pygame.quit()
sys.exit()