import pygame

FPS = 60

BLACK = (0,0,0)

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
        self.image.fill((255,0,0))
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

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#Running screen
running = True

while running :
    #Framerate by sec by screen
    clock.tick(FPS)
    # Pygame will register all events from the user
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    #Update
    all_sprites.update()

    #draw the colors on background
    screen.fill(BLACK)
    #draw all spirites on screen
    all_sprites.draw(screen)
    #draw the screen
    pygame.display.update()

pygame.quit()