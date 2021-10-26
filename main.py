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
        self.clock = pygame.time.Clock()                            #Framerate
        self.font = os.path.join("Text","font.ttf")
        self.running = True
        self.show_init = True
        self.Background_Img = pygame.image.load(os.path.join("Image","Background3.jpg")).convert()
        self.Background = pygame.transform.scale(self.Background_Img,(845,800))
        self.Background_Y = 0
        self.score = 0
        self.draw_screen = Draw_screen(self)
        self.hidden = False
        self.hide_time = 0

    def hide(self) :
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.player.kill()

    def new_game(self) :
        #A New game starts
        pygame.mixer.music.play(-1)
        """
        self.all_sprites = pygame.sprite.Group()
        self.Rocks = pygame.sprite.Group()
        self.Bullets = pygame.sprite.Group()
        self.Items = pygame.sprite.Group()
        self.the_boss = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for i in range(0,5) :
            self.new_rock()"""

    def new_rock(self) : 
        self.rock = Rock()
        self.all_sprites.add(self.rock)
        self.Rocks.add(self.rock)

    def new_boss1(self) :
        self.boss1 = Boss1(self)
        self.all_sprites.add(self.boss1)
        #self.the_boss.add(self.boss1)


    def events(self) :

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.running = False
            
            elif event.type == pygame.KEYDOWN :                                             #Press some key Down
                if event.key == pygame.K_SPACE :                                            #Press SPACE                                                
                    #self.player.shoot()                                                    #Player Shoot
                    pass

    def update(self) :
        
        self.all_sprites.update()

        now = pygame.time.get_ticks()

        if self.hidden and now - self.hide_time > 1000 :                                    #after 1 s we spawn player
            self.hidden = False
            self.all_sprites.add(self.player)
            self.player.rect.centerx = WIN_WIDTH / 2
            self.player.rect.bottom = WIN_HEIGHT - 50

        if self.player.live == 0 and not(self.death_expl.alive()):                          #Game over 
            #self.playing = False
            self.show_init = True

    def Collision(self) :

        #Rock and Bullets
        hits1 = pygame.sprite.groupcollide(self.Rocks, self.Bullets, True, True)             #Collision between Rock and Bullet, if they collide so we delete
        for i in hits1 :
            explo = Explosion(i.rect.center, 'big')
            self.all_sprites.add(explo)
            self.score += int(i.radius)
            random.choice(explo_sound).play()
            self.new_rock()

        #Player and Rock
        if self.player.health > 0 :                                                         #activate collision by checking if player still has health
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

        #Boss1 and Bullet
        if self.boss1.health > 1 :                                                          #activate collision by checking if boss still has health
            hits3 = pygame.sprite.spritecollide(self.boss1, self.Bullets, True, pygame.sprite.collide_mask)
            for i in hits3 :
                explo = Explosion(i.rect.center, 'big')
                self.all_sprites.add(explo)
                self.boss1.health -= 10
                if self.boss1.health < 1 :
                    pass
                    #self.all_sprites.remove(self.boss1)
                    #self.boss1.remove()

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
        self.draw_screen.Draw_live(self.screen, self.player.live, self.draw_screen.Player_Lives_Img, WIN_WIDTH - 100, 15)           #Draw Lives on screen

        self.clock.tick(FPS)                                                                #FPS by sec
        pygame.display.update()                                                             #Draw the screen

    def main(self) :
        
        self.main_menu()
        self.events()
        self.update()
        self.Collision()
        self.draw()

        #print(f"{self.clock.get_fps()} FPS")        #Show FPS in terminal
        

    def game_over(self) :
        pass

    def main_menu(self) :
        if self.show_init :
            close_game = self.draw_screen.Draw_init()
            if close_game :
                pass
            #A New game starts
            self.show_init = False
            self.all_sprites = pygame.sprite.Group()
            self.Rocks = pygame.sprite.Group()
            self.Bullets = pygame.sprite.Group()
            self.Items = pygame.sprite.Group()
            self.the_boss = pygame.sprite.Group()

            self.player = Player(self)
            self.all_sprites.add(self.player)

            for i in range(0,5) :
                self.new_rock()
            self.new_boss1()
            
game = Game()
game.new_game()

while game.running :
    game.main()

pygame.quit()
sys.exit()