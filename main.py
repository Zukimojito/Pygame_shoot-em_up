import pygame
import random
import os

from pygame.constants import K_d

FPS = 60

BLACK = (0,0,0)
RED = (255,0,0)
BROWN = (165,42,42)
TURQUOISE = (37,253,233)
WHITE = (255,255,255)
GREEN = (0,255,0)

width = 815
height = 895
#Initialize the game and create screen

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Python Game")       #Screen Name
clock = pygame.time.Clock()     #Framerate

Background_Img = pygame.image.load(os.path.join("Image","Background1.jpg")).convert()        #os.path mean in pygame file
Player_Img = pygame.image.load(os.path.join("Image","player.png")).convert()
Player_Lives_Img = pygame.image.load(os.path.join("Image","heart.png")).convert()
Player_Lives_heart = pygame.transform.scale(Player_Lives_Img,(25,25))
Player_Lives_heart.set_colorkey(WHITE)
Bullet_Img = pygame.image.load(os.path.join("Image","bullet.png")).convert()
Boss_Img = pygame.image.load(os.path.join("Image","boss.png")).convert()
# Rock_Img = pygame.image.load(os.path.join("Image","rock.png")).convert()
Rock_Imgs = []
for i in range(0,7) :
    Rock_Imgs.append(pygame.image.load(os.path.join("Image",f"rock{i}.png")).convert())

#explosion animation
explo_animation = {}
explo_animation['big'] = []
explo_animation['small'] = []
explo_animation['player'] = []
for i in range(9) :
    explo_img = pygame.image.load(os.path.join("Image",f"expl{i}.png")).convert()
    explo_img.set_colorkey(BLACK)
    explo_animation['big'].append(pygame.transform.scale(explo_img, (70,70)))
    explo_animation['small'].append(pygame.transform.scale(explo_img,(25,25)))

    player_explo_img = pygame.image.load(os.path.join("Image",f"player_expl{i}.png")).convert()
    player_explo_img.set_colorkey(BLACK)
    explo_animation['player'].append(pygame.transform.scale(player_explo_img,(150,150)))

item_drop = {}
item_drop['za_warudo'] = pygame.image.load(os.path.join("Image","item1.png")).convert()
item_drop['boost'] = pygame.image.load(os.path.join("Image","troll.png")).convert()

# Music & Sound
shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
death_sound = pygame.mixer.Sound(os.path.join("Sound","rumble.ogg"))
heal_sound = pygame.mixer.Sound(os.path.join("Sound","pow0.wav"))
boost_sound = pygame.mixer.Sound(os.path.join("Sound","pow1.wav"))

explo_sound = [
    pygame.mixer.Sound(os.path.join("Sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("Sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("Sound","background.ogg"))
pygame.mixer.music.set_volume(0.2)
shoot_sound.set_volume(0.2)
explo_sound[0].set_volume(0.2)
explo_sound[1].set_volume(0.2)
heal_sound.set_volume(0.1)
boost_sound.set_volume(0.1)

#font_name = pygame.font.match_font('Times New Roman')
font_name = os.path.join("Text","font.ttf")
def draw_text(surf, text, size, x, y) :
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock() : 
    rock = Rock()
    all_sprites.add(rock)
    Rock_collision.add(rock)

def new_boss() :
    boss = Boss()
    all_sprites.add(boss)
    Boss_collision.add(boss)

def draw_health(surf, hp, x, y) :
    if hp < 0 :
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 1)

def draw_lives(surf, lives, img, x, y) :
    for i in range(lives) :
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)

def Draw_init() :
    screen.blit(Background_Img,(0,0))
    draw_text(screen,'Swallowed Star', 64, width/2, height/4)
    draw_text(screen,'Press ← or → to move', 28, width/2, height/2)
    draw_text(screen,'Press SPACE to shoot', 28, width/2, height/1.5)
    draw_text(screen,'by Zukimojito', 12, width/1.075, height-20)
    pygame.display.update()
    waiting = True
    while waiting :
        clock.tick(FPS)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP :
                waiting = False
                return False

class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Player_Img,(50,35))
        self.image.set_colorkey(BLACK)          #remove black color in image
        #self.image = pygame.Surface((50,40))
        #self.image.fill(RED)
        self.radius = 20
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
        self.rect.centerx = width/2
        self.rect.bottom = height - 50
        self.speedX = 5
        self.speedY = 4
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = pygame.time.get_ticks()
        self.boost_level = 1
        self.boost_time = 0

    def update(self) :

        now = pygame.time.get_ticks()
        if self.boost_level > 1 and now - self.boost_time > 5000 :
            self.boost_level -= 1
            self.boost_time = now

        if self.hidden and now - self.hide_time >= 1000 :
            self.hidden = False
            self.rect.centerx = width/2
            self.rect.bottom = height - 50

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_q]: 
            self.rect.x -= self.speedX
        
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d] :
            self.rect.x += self.speedX

        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_z] :
            self.rect.y -= self.speedY
        
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s] :
            self.rect.y += self.speedY

        if self.rect.right > width :
            self.rect.right = width
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > height :
            self.rect.bottom = height
    
    def shoot(self) :

        if not(self.hidden) : # == False
            if self.boost_level == 1 :
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                Bullet_collision.add(bullet)
                shoot_sound.play()
            elif self.boost_level == 2 :
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                Bullet_collision.add(bullet1)
                Bullet_collision.add(bullet2)
                shoot_sound.play()
            elif self.boost_level >= 3 :
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                bullet3 = Bullet(self.rect.centerx,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                Bullet_collision.add(bullet1)
                Bullet_collision.add(bullet2)
                Bullet_collision.add(bullet3)
                shoot_sound.play()
    
    def hide(self) :
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (width/2, height+500)

    def boost(self) :
        self.boost_level += 1
        self.boost_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        #random_size_x = random.randrange(10,50)
        #random_size_y = random.randrange(10,50)
        self.image_original = random.choice(Rock_Imgs)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        #self.image = pygame.Surface((random_size_x,random_size_y))
        #self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0,width - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedX = random.randrange(-3,3)
        self.speedY = random.randrange(3,6)
        self.rotation_degree = random.randrange(-10,10)
        self.total_rotation_degree = 0

    def rotation(self) :

        self.total_rotation_degree += self.rotation_degree
        self.total_rotation_degree = self.total_rotation_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_rotation_degree)       #function to rotate
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self) :
        
        self.rotation()
        self.rect.y += self.speedY
        self.rect.x += self.speedX

        if self.rect.left > width or self.rect.right < 0 or self.rect.top > height :
            self.rect.x = random.randrange(0,width - self.rect.width)
            self.rect.y = random.randrange(-50,-20)
            self.speedX = random.randrange(-3,3)
            self.speedY = random.randrange(3,8)

class Boss(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image_original = Boss_Img
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        #self.rect.x = random.randrange(0,width - self.rect.width)
        self.position_x = random.randint(-250, width+250)     #position to reach x
        self.position_y = random.randint(-250, height + 250)
        self.rect.x = width/2 - int(self.rect.width/2)
        self.rect.y = 0
        self.speedX = random.randrange(3,5)
        self.speedY = random.randrange(3,5)
        self.rotation_degree = random.randrange(-10,10)
        self.total_rotation_degree = 0

    def rotation(self) :

        self.total_rotation_degree += self.rotation_degree
        self.total_rotation_degree = self.total_rotation_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_rotation_degree)       #function to rotate
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self) :

        if self.rect.x < self.position_x :
            self.rect.x += self.speedX
        elif self.rect.x > self.position_x :
            self.rect.x -= self.speedX
        if abs(self.rect.x - self.position_x) < self.speedX :
            self.position_x = random.randint(-250, width+250)

        if self.rect.y < self.position_y :
            self.rect.y += self.speedY
        elif self.rect.y > self.position_y :
            self.rect.y -= self.speedY
        if abs(self.rect.y - self.position_y) < self.speedY :
            self.position_y = random.randint(-250, height + 250)

        if self.rect.left > width + 150 or self.rect.right < 0 - 150 or self.rect.top > height + 150 or self.rect.bottom < 0 - 150:
            self.rect.x = random.choice([-100, width + 100])
            self.rect.y = random.randrange(-100,height + 150)
            self.speedX = random.randrange(3,5)
            self.speedY = random.randrange(3,5)


class Bullet(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = Bullet_Img
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

class Item(pygame.sprite.Sprite) :
    def __init__(self, center) : 
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['za_warudo','boost'])
        self.image = item_drop[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 4

    def update(self) :
        self.rect.y += self.speed
        if self.rect.top > height :
            self.kill

class Explosion(pygame.sprite.Sprite) :
    def __init__(self, center, size) :
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explo_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
    
    def update(self) :
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame == len(explo_animation[self.size]) :
                self.kill()
            else : 
                self.image = explo_animation[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

pygame.mixer.music.play()
#Running screen
show_init = True
running = True

while running :
    #Menu
    if show_init :
        close_game = Draw_init()
        if close_game :
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        Rock_collision = pygame.sprite.Group()
        Bullet_collision = pygame.sprite.Group()
        Item_collision = pygame.sprite.Group()
        Boss_collision = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        score_cap = 100
        boss_cap = 100
        maximum_rock = 2
        for i in range(0,7) :
            new_rock()

    #Framerate by sec by screen
    clock.tick(FPS)
    # Pygame will register all events from the user
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_j] : 
        player.shoot() 
        

    #Update
    all_sprites.update()
    Hit = pygame.sprite.groupcollide(Rock_collision,Bullet_collision,True,True)
    for i in Hit :
        random.choice(explo_sound).play()
        explo_anim = Explosion(i.rect.center, 'big')
        all_sprites.add(explo_anim)
        if random.random() > 0.80 :
            drop_item = Item(i.rect.center)
            all_sprites.add(drop_item)
            Item_collision.add(drop_item)
        new_rock()
        score += int(i.radius)
    if score > score_cap :
        new_rock()
        score_cap += 100
    if score > boss_cap :
        new_boss()
        boss_cap += 1000
            

    #Hit_boss = pygame.sprite.groupcollide(Boss_collision, Bullet_collision, True, True)
    #for i in Hit_boss :
        #random.choice(explo_sound).play()
        """
    hit_player_boss = pygame.sprite.spritecollide(player, Boss_collision, True, pygame.sprite.collide_circle)
    for i in hit_player_boss :
        player.health -= 100
        if player.health <= 0 :
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            death_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()"""

    hit_player_rock = pygame.sprite.spritecollide(player, Rock_collision, True, pygame.sprite.collide_circle)
    for i in hit_player_rock :
        new_rock()
        player.health -= i.radius
        explo_anim = Explosion(i.rect.center, 'small')
        all_sprites.add(explo_anim)
        if player.health <= 0 :
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            death_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
    #Collision Player and Item
    hit_item = pygame.sprite.spritecollide(player, Item_collision, True)
    for i in hit_item :
        if i.type == 'za_warudo' :
            player.health += 10
            if player.health > 100 :
                player.health = 100
            heal_sound.play()
        elif i.type == 'boost' :
            player.boost()
            boost_sound.play()

    if player.lives == 0 and not(death_expl.alive()):
        #running = False
        show_init = True

    #draw the colors on background
    screen.fill(BLACK)
    screen.blit(Background_Img,(0,0))
    #draw all spirites on screen
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, width/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_lives(screen,player.lives,Player_Lives_heart,width-100, 15)
    #draw the screen
    pygame.display.update()

pygame.quit()