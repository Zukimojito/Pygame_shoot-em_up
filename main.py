import pygame
import random

FPS = 60

BLACK = (0,0,0)
RED = (255,0,0)
BROWN = (165,42,42)
TURQUOISE = (37,253,233)

width = 500
height = 600

#Initialize the game and create screen

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Python Game")       #Screen Name
clock = pygame.time.Clock()     #Framerate

class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = height - 50
        self.speedX = 5
    
    def update(self) :

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] : 
            self.rect.x -= self.speedX
        
        if key_pressed[pygame.K_RIGHT] :
            self.rect.x += self.speedX

        if self.rect.right > width : 
            self.rect.right = width
        if self.rect.left < 0 :
            self.rect.left = 0
    
    def shoot(self) :
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)

class Rock(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        random_size_x = random.randrange(10,50)
        random_size_y = random.randrange(10,50)
        self.image = pygame.Surface((random_size_x,random_size_y))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width - self.rect.width)
        self.rect.y = random.randrange(-50,-20)
        self.speedX = random.randrange(-3,3)
        self.speedY = random.randrange(3,8)
    
    def update(self) :
        self.rect.y += self.speedY
        self.rect.x += self.speedX

        if self.rect.left > width or self.rect.right < 0 or self.rect.top > height :
            self.rect.x = random.randrange(0,width - self.rect.width)
            self.rect.y = random.randrange(-50,-20)
            self.speedX = random.randrange(-3,3)
            self.speedY = random.randrange(3,8)

class Bullet(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(TURQUOISE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = -10

    def update(self) :
        self.rect.y += self.speedY
        if self.rect.bottom < 0 :
            self.kill()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(0,10) :
    rock = Rock()
    all_sprites.add(rock)

#Running screen
running = True

while running :
    #Framerate by sec by screen
    clock.tick(FPS)
    # Pygame will register all events from the user
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # key_pressed = pygame.key.get_pressed()
    # if key_pressed[pygame.K_j] : 
    #   player.shoot()

    #Update
    all_sprites.update()

    #draw the colors on background
    screen.fill(BLACK)
    #draw all spirites on screen
    all_sprites.draw(screen)
    #draw the screen
    pygame.display.update()

pygame.quit()